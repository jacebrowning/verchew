Unix: [![Unix Build Status](https://img.shields.io/travis/jacebrowning/verchew/develop.svg)](https://travis-ci.org/jacebrowning/verchew) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/verchew/develop.svg)](https://ci.appveyor.com/project/jacebrowning/verchew)<br>Metrics: [![Coverage Status](https://img.shields.io/coveralls/jacebrowning/verchew/develop.svg)](https://coveralls.io/r/jacebrowning/verchew) [![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/verchew.svg)](https://scrutinizer-ci.com/g/jacebrowning/verchew/?branch=develop)<br>Usage: [![PyPI Version](https://img.shields.io/pypi/v/verchew.svg)](https://pypi.python.org/pypi/verchew) [![PyPI Downloads](https://img.shields.io/pypi/dm/verchew.svg)](https://pypi.python.org/pypi/verchew)

# Overview

Verchew is an embeddable Python script to check the versions of your project's system dependencies. Its only external dependency is a Python interpreter, available on macOS and most linux-based operating systems.

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

Create a configuration file (`.verchew`) with your project's system dependencies:

```ini
[Working Program]

cli = working-program
version = 1.2.

[Newer Working Program]

cli = working-program
version =  4.

[Broken Program]

cli = broken-program
version = 1.2.3

[Missing Program]

cli = missing-program
version = 1.2.3
```

Run `verchew` to see if you have the right versions installed:

```sh
$ verchew

Checking for Working Program...

$ working-program --version
1.2.3
✔ MATCHED: 1.2.

Checking for Newer Working Program...

$ working-program --version
1.2.3
✘ EXPECTED: 4.

Checking for Broken Program...

$ broken-program --version
An error occurred.
✘ EXPECTED: 1.2.3

Checking for Missing Program...

$ missing-program --version
sh: command not found: missing-program
✘ EXPECTED: 1.2.3

Results: ✔ ✘ ✘ ✘
```
