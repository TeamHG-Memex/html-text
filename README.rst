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
adding spaces around inline elements too
(which are often used as block elements in html markup),
and tries to avoid adding extra spaces for punctuation.

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
    >>> text = html_text.extract_text(u'<h1>Hey</h1>')
    u'Hey'

You can also pass already parsed ``lxml.html.HtmlElement``:

    >>> import html_text
    >>> tree = html_text.parse_html(u'<h1>Hey</h1>')
    >>> text = html_text.extract_text(tree)
    u'Hey'


Credits
-------

The code is extracted from utilities used in several projects, written by Mikhail Korobov.
