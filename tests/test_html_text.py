# -*- coding: utf-8 -*-
import pytest
import glob

from html_text import (extract_text, parse_html, cleaned_selector,
                       selector_to_text, NEWLINE_TAGS, DOUBLE_NEWLINE_TAGS)


@pytest.fixture(params=[
    {'guess_punct_space': True, 'guess_layout': False},
    {'guess_punct_space': False, 'guess_layout': False},
    {'guess_punct_space': True, 'guess_layout': True},
    {'guess_punct_space': False, 'guess_layout': True}
])
def all_options(request):
    return request.param


def test_extract_no_text_html(all_options):
    html = (u'<!DOCTYPE html><html><body><p><video width="320" height="240" '
            'controls><source src="movie.mp4" type="video/mp4"><source '
            'src="movie.ogg" type="video/ogg"></video></p></body></html>')
    assert extract_text(html, **all_options) == u''


def test_extract_text(all_options):
    html = (u'<html><style>.div {}</style>'
            '<body><p>Hello,   world!</body></html>')
    assert extract_text(html, **all_options) == u'Hello, world!'


def test_declared_encoding(all_options):
    html = (u'<?xml version="1.0" encoding="utf-8" ?>'
            u'<html><style>.div {}</style>'
            u'<body>Hello,   world!</p></body></html>')
    assert extract_text(html, **all_options) == u'Hello, world!'


def test_empty(all_options):
    assert extract_text(u'', **all_options) == ''


def test_extract_text_from_tree(all_options):
    html = (u'<html><style>.div {}</style>'
            '<body><p>Hello,   world!</body></html>')
    tree = parse_html(html)
    assert extract_text(tree, **all_options) == u'Hello, world!'


def test_inline_tags_whitespace(all_options):
    html = u'<span>field</span><span>value  of</span><span></span>'
    assert extract_text(html, **all_options) == u'field value of'


def test_punct_whitespace():
    html = u'<div><span>field</span>, and more</div>'
    assert extract_text(html, guess_punct_space=False) == u'field , and more'
    assert extract_text(html, guess_punct_space=True) == u'field, and more'


def test_punct_whitespace_preserved():
    html = (u'<div><span>по</span><span>ле</span>, and  ,  '
            u'<span>more </span>!<span>now</div>a (<b>boo</b>)')
    text = extract_text(html, guess_punct_space=True, guess_layout=False)
    assert text == u'по ле, and , more ! now a (boo)'


@pytest.mark.xfail(reason="code punctuation should be handled differently")
def test_bad_punct_whitespace():
    html = (u'<pre><span>trees</span> '
            '<span>=</span> <span>webstruct</span>'
            '<span>.</span><span>load_trees</span>'
            '<span>(</span><span>&quot;train/*.html&quot;</span>'
            '<span>)</span></pre>')
    text = extract_text(html, guess_punct_space=False, guess_layout=False)
    assert text == u'trees = webstruct . load_trees ( "train/*.html" )'

    text = extract_text(html, guess_punct_space=True, guess_layout=False)
    assert text == u'trees = webstruct.load_trees("train/*.html")'


def test_selector(all_options):
    html = (u'<span><span id="extract-me">text<a>more</a>'
            '</span>and more text <a> and some more</a> <a></a> </span>')
    sel = cleaned_selector(html)
    assert selector_to_text(sel, **all_options) == 'text more and more text and some more'
    subsel = sel.xpath('//span[@id="extract-me"]')
    assert selector_to_text(subsel, **all_options) == 'text more'
    subsel = sel.xpath('//a')
    assert selector_to_text(subsel, **all_options) == 'more and some more'
    subsel = sel.xpath('//a[@id="extract-me"]')
    assert selector_to_text(subsel, **all_options) == ''


def test_guess_layout():
    html = (u'<title>  title  </title><div>text_1.<p>text_2 text_3</p>'
            '<p id="demo"></p><ul><li>text_4</li><li>text_5</li></ul>'
            '<p>text_6<em>text_7</em>text_8</p>text_9</div>'
            '<script>document.getElementById("demo").innerHTML = '
            '"This should be skipped";</script> <p>...text_10</p>')

    text = 'title text_1. text_2 text_3 text_4 text_5 text_6 text_7 ' \
           'text_8 text_9 ...text_10'
    assert extract_text(html, guess_punct_space=False, guess_layout=False) == text

    text = ('title\n\n text_1.\n\n text_2 text_3\n\n text_4\n text_5'
            '\n\n text_6 text_7 text_8\n\n text_9\n\n ...text_10')
    assert extract_text(html, guess_punct_space=False, guess_layout=True) == text

    text = 'title text_1. text_2 text_3 text_4 text_5 text_6 text_7 ' \
           'text_8 text_9...text_10'
    assert extract_text(html, guess_punct_space=True, guess_layout=False) == text

    text = 'title\n\ntext_1.\n\ntext_2 text_3\n\ntext_4\ntext_5\n\n' \
           'text_6 text_7 text_8\n\ntext_9\n\n...text_10'
    assert extract_text(html, guess_punct_space=True, guess_layout=True) == text


def test_adjust_newline():
    html = u'<div>text 1</div><p><div>text 2</div></p>'
    assert extract_text(html, guess_layout=True) == 'text 1\n\ntext 2'


def test_personalize_newlines_sets():
    html = (u'<span><span>text<a>more</a>'
            '</span>and more text <a> and some more</a> <a></a> </span>')

    text = extract_text(html, guess_layout=True,
                        newline_tags=NEWLINE_TAGS | {'a'})
    assert text == 'text\nmore\nand more text\nand some more'

    text = extract_text(html, guess_layout=True,
                        double_newline_tags=DOUBLE_NEWLINE_TAGS | {'a'})
    assert text == 'text\n\nmore\n\nand more text\n\nand some more'


def test_webpages():
    webpages = sorted(glob.glob('./test_webpages/*.html'))
    extracted = sorted(glob.glob('./test_webpages/*.txt'))
    for page, extr in zip(webpages, extracted):
        with open(page, 'r', encoding='utf8') as f_in:
            html = f_in.read()
        with open(extr, 'r', encoding='utf8') as f_in:
            expected = f_in.read()
        assert extract_text(html) == expected
