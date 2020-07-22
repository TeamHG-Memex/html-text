#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as history_file:
    history = history_file.read()


setup(
    name='html_text',
    version='0.5.2',
    description="Extract text from HTML",
    long_description=readme + '\n\n' + history,
    author="Konstantin Lopukhin",
    author_email='kostia.lopuhin@gmail.com',
    url='https://github.com/TeamHG-Memex/html-text',
    packages=['html_text'],
    include_package_data=True,
    install_requires=['lxml'],
    license="MIT license",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=['pytest'],
)
