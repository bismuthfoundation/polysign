#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pycryptodomex', 'ed25519', 'base58', 'coincurve']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="EggdraSyl from Bismuth Foundation",
    author_email='dev@eggpool.net',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Polysign PIP module for Bismuth. Handles the various cryptographic primitives Bismuth Crypto currency supports.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='polysign',
    name='Polysign',
    packages=find_packages(include=['polysign']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bismuthfoundation/polysign',
    version='0.1.0',
    zip_safe=False,
)
