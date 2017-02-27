# -*- coding: utf-8 -*-
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


def selector_to_text(sel):
    """ Convert a cleaned selector to text.
    """
    return sel.xpath('normalize-space()').extract_first('')


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


def extract_text(html, encoding='utf8'):
    """
    Convert html to text.

    html should be a unicode string or an already parsed lxml.html element.
    """
    return selector_to_text(cleaned_selector(html))
