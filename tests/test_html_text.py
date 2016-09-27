# -*- coding: utf-8 -*-

from html_text import extract_text


def test_extract_text():
    html = u'<html><style>.div {}</style><body><p>Hello,   world!</body></html>'
    assert extract_text(html) == u'Hello, world!'


def test_declared_encoding():
    html = (u'<?xml version="1.0" encoding="utf-8" ?>'
            u'<html><style>.div {}</style>'
            u'<body>Hello,   world!</p></body></html>')
    assert extract_text(html) == u'Hello, world!'


def test_empty():
    assert extract_text(u'') == ''

