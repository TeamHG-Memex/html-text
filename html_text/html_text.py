# -*- coding: utf-8 -*-
import re

import lxml
import lxml.etree
from lxml.html.clean import Cleaner
import parsel


_clean_html = Cleaner(
    scripts=True,
    javascript=False,  # onclick attributes are fine
    comments=True,
    style=True,
    links=True,
    meta=True,
    page_structure=False,  # <title> may be nice to have
    processing_instructions=True,
    embedded=True,
    frames=True,
    forms=False,  # keep forms
    annoying_tags=False,
    remove_unknown_tags=False,
    safe_attrs_only=False,
).clean_html


def _cleaned_html_tree(html):
    if isinstance(html, lxml.html.HtmlElement):
        tree = html
    else:
        parser = lxml.html.HTMLParser(encoding='utf8')
        tree = lxml.html.fromstring(html.encode('utf8'), parser=parser)
    return _clean_html(tree)


def parse_html(html):
    """ Create an lxml.html.HtmlElement from a string with html.
    """
    parser = lxml.html.HTMLParser(encoding='utf8')
    return lxml.html.fromstring(html.encode('utf8'), parser=parser)


_whitespace = re.compile(r'\s+')
_has_trailing_whitespace = re.compile(r'\s$').search
_has_punct_after = re.compile(r'^[,:;.!?"\)]').search
_has_punct_before = re.compile(r'\($').search


def selector_to_text(sel, guess_punct_space=True):
    """ Convert a cleaned selector to text.
    See html_text.extract_text docstring for description of the approach and options.
    """
    if guess_punct_space:

        def fragments():
            prev = None
            for text in sel.xpath('//text()').extract():
                if prev is not None and (_has_trailing_whitespace(prev)
                                         or (not _has_punct_after(text) and
                                             not _has_punct_before(prev))):
                    yield ' '
                yield text
                prev = text

        return _whitespace.sub(' ', ''.join(fragments()).strip())

    else:
        fragments = (x.strip() for x in sel.xpath('//text()').extract())
        return _whitespace.sub(' ', ' '.join(x for x in fragments if x))


def cleaned_selector(html):
    """ Clean selector.
    """
    try:
        tree = _cleaned_html_tree(html)
        sel = parsel.Selector(root=tree, type='html')
    except (lxml.etree.XMLSyntaxError,
            lxml.etree.ParseError,
            lxml.etree.ParserError,
            UnicodeEncodeError):
        # likely plain text
        sel = parsel.Selector(html)
    return sel


def extract_text(html, guess_punct_space=True):
    """
    Convert html to text.
    Almost the same as normalize-space xpath, but this also
    adds spaces between inline elements (like <span>) which are
    often used as block elements in html markup.

    When guess_punct_space is True (default), no extra whitespace is added
    for punctuation. This has a slight (around 10%) performance overhead
    and is just a heuristic.

    html should be a unicode string or an already parsed lxml.html element.
    """
    sel = cleaned_selector(html)
    return selector_to_text(sel, guess_punct_space=guess_punct_space)
