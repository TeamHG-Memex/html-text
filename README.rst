============
HTML to Text
============


.. image:: https://img.shields.io/pypi/v/html_text.svg
        :target: https://pypi.python.org/pypi/html_text

.. image:: https://img.shields.io/travis/TeamHG-Memex/html_text.svg
        :target: https://travis-ci.org/TeamHG-Memex/html_text

.. image:: https://readthedocs.org/projects/html-text/badge/?version=latest
        :target: https://html-text.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Extract text from HTML


* Free software: MIT license
* Documentation: https://html-text.readthedocs.io.


Features
--------

Extract text from HTML::

    >>> import html_text
    >>> text = html_text.extract_text(u'<h1>Hey</h1>')
    u'Hey'


Credits
-------

The code is extracted from utilities used in several projects, written by Mikhail Korobov.
