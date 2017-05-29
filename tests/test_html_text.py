# -*- coding: utf-8 -*-
import pytest

from html_text import extract_text, parse_html


@pytest.fixture(params=[{'guess_punct_space': True},
                        {'guess_punct_space': False}])
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
    assert (extract_text(html, guess_punct_space=True) ==
            u'по ле, and , more ! now a (boo)')
