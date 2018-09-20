=======
History
=======

0.4.0 TDB
------------------

* Add ``guess_page_layout`` to make extracted text look like how it is rendered
  in browser.
* Add tests of layout extraction for real webpages.


0.3.0 (2017-10-12)
------------------

* Expose functions that operate on selectors,
  use ``.//text()`` to extract text from selector.


0.2.1 (2017-05-29)
------------------

* Packaging fix (include CHANGES.rst)


0.2.0 (2017-05-29)
------------------

* Fix unwanted joins of words with inline tags: spaces are added for inline
  tags too, but a heuristic is used to preserve punctuation without extra spaces.
* Accept parsed html trees.


0.1.1 (2017-01-16)
------------------

* Travis-CI and codecov.io integrations added


0.1.0 (2016-09-27)
------------------

* First release on PyPI.
