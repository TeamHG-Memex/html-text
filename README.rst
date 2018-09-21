============
HTML to Text
============


.. image:: https://img.shields.io/pypi/v/html-text.svg
   :target: https://pypi.python.org/pypi/html-text
   :alt: PyPI Version

.. image:: https://img.shields.io/travis/TeamHG-Memex/html-text.svg
   :target: https://travis-ci.org/TeamHG-Memex/html-text
   :alt: Build Status

.. image:: http://codecov.io/github/TeamHG-Memex/soft404/coverage.svg?branch=master
   :target: http://codecov.io/github/TeamHG-Memex/html-text?branch=master
   :alt: Code Coverage

Extract text from HTML


* Free software: MIT license


How is html_text different from ``.xpath('//text()')`` from LXML
or ``.get_text()`` from Beautiful Soup?
Text extracted with ``html_text`` does not contain inline styles,
javascript, comments and other text that is not normally visible to the users.
It normalizes whitespace, but is also smarter than ``.xpath('normalize-space())``,
adding spaces around inline elements (which are often used as block
elements in html markup), tries to avoid adding extra spaces for punctuation and
can add newlines so that the output text looks like how it is rendered in
browsers.

Apart from just getting text from the page (e.g. for display or search),
one intended usage of this library is for machine learning (feature extraction).
If you want to use the text of the html page as a feature (e.g. for classification),
this library gives you plain text that you can later feed into a standard text
classification pipeline.
If you feel that you need html structure as well, check out
`webstruct <http://webstruct.readthedocs.io/en/latest/>`_ library.


Install
-------

Install with pip::

    pip install html-text

The package depends on lxml, so you might need to install some additional
packages: http://lxml.de/installation.html


Usage
-----

Extract text from HTML::

    >>> import html_text
    >>> html_text.extract_text('<h1>Hello</h1> world!')
    'Hello world!'

    >>> html_text.extract_text(u'<h1>Hello</h1> world!', guess_page_layout=True)
    'Hello\n\nworld!'


You can also pass already parsed ``lxml.html.HtmlElement``:

    >>> import html_text
    >>> tree = html_text.parse_html('<h1>Hello</h1> world!')
    >>> html_text.extract_text(tree)
    'Hello world!'

Or define a selector to extract text only from specific elements:

    >>> import html_text
    >>> sel = html_text.cleaned_selector('<h1>Hello</h1> world!')
    >>> subsel = sel.xpath('//h1')
    >>> html_text.selector_to_text(subsel)
    'Hello'

Passed html will be first cleaned from invisible non-text content such
as styles, and then text would be extracted.
NB Selectors are not cleaned automatically you need to call
``html_text.cleaned_selector`` first.

Main functions:

* ``html_text.extract_text`` accepts html and returns extracted text.
* ``html_text.cleaned_selector`` accepts html as text or as ``lxml.html.HtmlElement``,
  and returns cleaned ``parsel.Selector``.
* ``html_text.selector_to_text`` accepts ``parsel.Selector`` and returns extracted
  text.

If ``guess_page_layout`` is True (False by default for backward compatibility),
a newline is added before and after ``newline_tags`` and two newlines are added
before and after ``double_newline_tags``. This heuristic makes the extracted text
more similar to how it is rendered in the browser. Default newline and double
newline tags can be found in `html_text.NEWLINE_TAGS`
and `html_text.DOUBLE_NEWLINE_TAGS`.

It is possible to customize how newlines are added, using ``newline_tags`` and
``double_newline_tags`` arguments (which are `html_text.NEWLINE_TAGS` and
`html_text.DOUBLE_NEWLINE_TAGS` by default). For example, don't add a newline
after ``<div>`` tags:

    >>> newline_tags = html_text.NEWLINE_TAGS - {'div'}
    >>> html_text.extract_text('<div>Hello</div> world!',
    ...                        guess_page_layout=True,
    ...                        newline_tags=newline_tags)
    'Hello world!'

Credits
-------

The code is extracted from utilities used in several projects, written by Mikhail Korobov.

----

.. image:: https://hyperiongray.s3.amazonaws.com/define-hg.svg
	:target: https://www.hyperiongray.com/?pk_campaign=github&pk_kwd=html-text
	:alt: define hyperiongray
