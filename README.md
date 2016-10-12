Unix: [![Unix Build Status](https://img.shields.io/travis/jacebrowning/verchew/develop.svg)](https://travis-ci.org/jacebrowning/verchew) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/verchew/develop.svg)](https://ci.appveyor.com/project/jacebrowning/verchew)<br>Metrics: [![Coverage Status](https://img.shields.io/coveralls/jacebrowning/verchew/develop.svg)](https://coveralls.io/r/jacebrowning/verchew) [![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/verchew.svg)](https://scrutinizer-ci.com/g/jacebrowning/verchew/?branch=develop)<br>Usage: [![PyPI Version](https://img.shields.io/pypi/v/verchew.svg)](https://pypi.python.org/pypi/verchew) [![PyPI Downloads](https://img.shields.io/pypi/dm/verchew.svg)](https://pypi.python.org/pypi/verchew)

# Overview

This is an embeddable Python script to check the versions of your system dependencies.

# Setup

## Requirements

* Python 2.7+ or Python 3.3+

## Installation

Install verchew with pip:

```sh
$ pip install verchew
```

or directly from the source code:

```sh
$ git clone https://github.com/jacebrowning/verchew.git
$ cd verchew
$ python setup.py install
```

# Usage

After installation, the package can imported:

```sh
$ python
>>> import verchew
>>> verchew.__version__
```
