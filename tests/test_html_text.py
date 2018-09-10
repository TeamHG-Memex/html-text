# -*- coding: utf-8 -*-
import pytest
import lxml

from html_text import (extract_text, parse_html, cleaned_selector,
                       selector_to_text)


@pytest.fixture(params=[{
    'guess_punct_space': True
}, {
    'guess_punct_space': False
}, {
    'guess_punct_space': True,
    'guess_page_layout': True
}, {
    'guess_punct_space': False,
    'guess_page_layout': True
}])
def all_options(request):
    return request.param


def test_extract_text(all_options):
    html = u'<html><style>.div {}</style><body><p>Hello,   world!</body></html>'
    assert extract_text(html, **all_options) == u'Hello, world!'


def test_declared_encoding(all_options):
    html = (u'<?xml version="1.0" encoding="utf-8" ?>'
            u'<html><style>.div {}</style>'
            u'<body>Hello,   world!</p></body></html>')
    assert extract_text(html, **all_options) == u'Hello, world!'


def test_empty(all_options):
    assert extract_text(u'', **all_options) == ''


def test_extract_text_from_tree(all_options):
    html = u'<html><style>.div {}</style><body><p>Hello,   world!</body></html>'
    tree = parse_html(html)
    assert extract_text(tree, **all_options) == u'Hello, world!'


def test_inline_tags_whitespace(all_options):
    html = u'<span>field</span><span>value  of</span><span></span>'
    assert extract_text(html, **all_options) == u'field value of'


def test_punct_whitespace():
    html = u'<div><span>field</span>, and more</div>'
    assert extract_text(html, guess_punct_space=False) == u'field , and more'


def test_punct_whitespace_preserved():
    html = (u'<div><span>по</span><span>ле</span>, and  ,  '
            u'<span>more </span>!<span>now</div>a (<b>boo</b>)')
    assert (extract_text(
        html, guess_punct_space=True) == u'по ле, and , more ! now a (boo)')


def test_selector(all_options):
    html = '<div><div id="extract-me">text<div>more</div></div>and more text</div>'
    sel = cleaned_selector(html)
    assert selector_to_text(sel, **all_options) == 'text more and more text'
    subsel = sel.xpath('//div[@id="extract-me"]')[0]
    assert selector_to_text(subsel, **all_options) == 'text more'

#
# def test_guess_page_layout():
#     html = (u'<title>  title  </title><div>text_1.<p>text_2 text_3</p>'
#             '<p id="demo"></p><ul><li>text_4</li><li>text_5</li></ul>'
#             '<p>text_6<em>text_7</em>text_8</p>text_9</div>'
#             '<script>document.getElementById("demo").innerHTML = '
#             '"This should be skipped";</script> <p>...text_10</p>')
#     assert (extract_text(html, guess_punct_space=False) == (
#         'title text_1. text_2 text_3 text_4 text_5'
#         ' text_6 text_7 text_8 text_9 ...text_10'))
#     assert (extract_text(
#         html, guess_punct_space=False, guess_page_layout=True) == (
#             'title\n\n text_1.\n\n text_2 text_3\n\n text_4\n text_5'
#             '\n\n text_6 text_7 text_8\n\n text_9\n\n ...text_10'))
#     assert (extract_text(
#         html,
#         guess_punct_space=True) == ('title text_1. text_2 text_3 text_4 text_5'
#                                     ' text_6 text_7 text_8 text_9...text_10'))
#     assert (extract_text(
#         html, guess_punct_space=True, guess_page_layout=True) == (
#             'title\n\ntext_1.\n\ntext_2 text_3\n\ntext_4\ntext_5'
#             '\n\ntext_6 text_7 text_8\n\ntext_9\n\n...text_10'))
