# -*- coding: utf-8 -*-
import re

import lxml
import lxml.etree
from lxml.html.clean import Cleaner
import parsel

NEWLINE_TAGS = frozenset(['li', 'dd', 'dt', 'dl', 'ul', 'ol'])
DOUBLE_NEWLINE_TAGS = frozenset(
    ['title', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

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
_has_open_bracket_before = re.compile(r'\($').search


def html_to_text(tree, guess_punct_space=True, guess_page_layout=False):
    """
    Convert a cleaned html tree to text.
    See html_text.extract_text docstring for description of the approach
    and options.
    """

    def add_space(text, prev):
        if prev is None:
            return False
        if prev == '\n' or prev == '\n\n':
            return False
        if not _has_trailing_whitespace(prev):
            if _has_punct_after(text) or _has_open_bracket_before(prev):
                return False
        return True

    def add_newline(tag, prev):
        if prev is None or prev == '\n\n':
            return ''
        if tag in DOUBLE_NEWLINE_TAGS:
            if prev == '\n':
                return '\n'
            return '\n\n'
        if tag in NEWLINE_TAGS:
            if prev == '\n':
                return ''
            return '\n'
        return ''

    def traverse_text_fragments(tree, prev, depth):
        space = ' '
        newline = ''
        if tree.text:
            text = _whitespace.sub(' ', tree.text.strip())
            if text:
                if guess_page_layout:
                    newline = add_newline(tree.tag, prev[0])
                    if newline:
                        prev[0] = newline
                if guess_punct_space and not add_space(text, prev[0]):
                    space = ''
                yield [newline, space, text]
                prev[0] = tree.text
                space = ' '
                newline = ''

        for child in tree:
            for t in traverse_text_fragments(child, prev, depth + 1):
                yield t

        if guess_page_layout:
            newline = add_newline(tree.tag, prev[0])
            if newline:
                prev[0] = newline

        tail = ''
        if tree.tail and depth != 0:
            tail = _whitespace.sub(' ', tree.tail.strip())
            if tail:
                if guess_punct_space and not add_space(tail, prev[0]):
                    space = ''
        if tail:
            yield [newline, space, tail]
            prev[0] = tree.tail
        elif newline:
            yield [newline]

    text = []
    for fragment in traverse_text_fragments(tree, [None], 0):
        text.extend(fragment)
    return ''.join(text).strip()


def selector_to_text(sel, guess_punct_space=True, guess_page_layout=False):
    """ Convert a cleaned selector to text.
    See html_text.extract_text docstring for description of the approach
    and options.
    """
    return html_to_text(
        sel.root,
        guess_punct_space=guess_punct_space,
        guess_page_layout=guess_page_layout)


def cleaned_selector(html):
    """ Clean selector.
    """
    try:
        tree = _cleaned_html_tree(html)
        sel = parsel.Selector(root=tree, type='html')
    except (lxml.etree.XMLSyntaxError, lxml.etree.ParseError,
            lxml.etree.ParserError, UnicodeEncodeError):
        # likely plain text
        sel = parsel.Selector(html)
    return sel


def extract_text(html,
                 guess_punct_space=True,
                 guess_page_layout=False,
                 newline_tags=NEWLINE_TAGS,
                 double_newline_tags=DOUBLE_NEWLINE_TAGS):
    """
    Convert html to text, cleaning invisible content such as styles.
    Almost the same as normalize-space xpath, but this also
    adds spaces between inline elements (like <span>) which are
    often used as block elements in html markup.

    When guess_punct_space is True (default), no extra whitespace is added
    for punctuation. This has a slight (around 10%) performance overhead
    and is just a heuristic.

    When guess_page_layout is True (default is False), a newline is added after
    NEWLINE_TAGS and two newlines after DOUBLE_NEWLINE_TAGS. This heuristic
    makes the extracted text more similar to how it looks like in the browser.

    NEWLINE_TAGS and DOUBLE_NEWLINE_TAGS can be customized.

    html should be a unicode string or an already parsed lxml.html element.
    """
    if html is None or len(html) == 0:
        return ''
    cleaned = _cleaned_html_tree(html)
    return html_to_text(
        cleaned,
        guess_punct_space=guess_punct_space,
        guess_page_layout=guess_page_layout,
        newline_tags=newline_tags,
        double_newline_tags=double_newline_tags,
    )
