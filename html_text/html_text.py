# -*- coding: utf-8 -*-
import re

import lxml
import lxml.etree
from lxml.html.clean import Cleaner


NEWLINE_TAGS = ['title', 'p', 'li', 'dd', 'dt', 'dl', 'ul',
                'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

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
    """ Convert a cleaned html tree to text.
        See html_text.extract_text docstring for description of the approach
        and options.
    """

    def add_space(text, prev):
        # return True if a space should be added
        if prev == '\n':
            return False
        return (prev is not None
                and (_has_trailing_whitespace(prev)
                     or (not _has_punct_after(text)
                     and not _has_open_bracket_before(prev)
                          )
                     )
                )

    def add_newline(tag, prev):
        return tag in NEWLINE_TAGS and prev != '\n'

    def traverse_text_fragments(tree, prev):
        space = ' '
        if tree.text:
            text = _whitespace.sub(' ', tree.text.strip())
            if text:
                if guess_punct_space and not add_space(text, prev[0]):
                    space = ''
                yield [space, text]
                prev[0] = tree.text
                space = ' '

        for child in tree:
            for t in traverse_text_fragments(child, prev):
                yield t

        newline = ''
        if guess_page_layout and add_newline(tree.tag, prev[0]):
            newline = '\n'
            prev[0] = '\n'

        tail = ''
        if tree.tail:
            tail = _whitespace.sub(' ', tree.tail.strip())
            if tail:
                if (guess_punct_space
                    and (not add_space(tail, prev[0]) or newline)):
                    space = ''

        if tail:
            yield [newline, space, tail]
            prev[0] = tree.tail
        elif newline:
            yield [newline]

    text = []
    for fragment in traverse_text_fragments(tree, [None]):
        text.extend(fragment)
    return ''.join(text).strip()



def extract_text(html, guess_punct_space=True, guess_page_layout=False, new=True):
    """
    Convert html to text, cleaning invisible content such as styles.
    Almost the same as normalize-space xpath, but this also
    adds spaces between inline elements (like <span>) which are
    often used as block elements in html markup.

    When guess_punct_space is True (default), no extra whitespace is added
    for punctuation. This has a slight (around 10%) performance overhead
    and is just a heuristic.

    html should be a unicode string or an already parsed lxml.html element.
    """
    if html is None or len(html) == 0:
        return ''
    cleaned = _cleaned_html_tree(html)
    return html_to_text(cleaned, guess_punct_space=guess_punct_space, guess_page_layout=guess_page_layout)
