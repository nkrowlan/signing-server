#!/usr/bin/env python
from setuptools import setup

setup(
    name="signing-server",
    version="0.0.1",
    description="A simple signed request/response protocol server.",
    author="nathan",
    author_email="nathan@helo.org",
    url="https://github.com/nkrowlan/signing-server",
    keywords=["twisted", "signing", "demo"],
    packages=["signing"],
    install_requires=["twisted>=14.0"],
    license="Apache License, Version 2.0",
    test_suite="trial",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Framework :: Twisted",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet"]
    )
