#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as history_file:
    history = history_file.read()

requirements = [
    'lxml',
    'parsel',
]

test_requirements = [
    'pytest',
]

setup(
    name='html_text',
    version='0.4.0',
    description="Extract text from HTML",
    long_description=readme + '\n\n' + history,
    author="Konstantin Lopukhin",
    author_email='kostia.lopuhin@gmail.com',
    url='https://github.com/TeamHG-Memex/html-text',
    packages=['html_text'],
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
