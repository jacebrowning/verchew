# Overview

> ...chews through your system dependencies, spitting out incompatible versions.

When onboarding new team members, ensuring their computer has everything needed to work on the project can be painful. Verchew is a command-line program and embeddable Python script to check the versions of your project's system dependencies. Its only external dependency is any Python interpreter, which should already be installed on macOS and most Linux-based operating systems.

[![Travis CI](https://img.shields.io/travis/com/jacebrowning/verchew/main.svg?label=unix)](https://app.travis-ci.com/jacebrowning/verchew)
[![AppVeyor](https://img.shields.io/appveyor/ci/jacebrowning/verchew/main.svg?label=windows)](https://ci.appveyor.com/project/jacebrowning/verchew)
[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/verchew/main.svg)](https://coveralls.io/r/jacebrowning/verchew)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/verchew.svg)](https://scrutinizer-ci.com/g/jacebrowning/verchew/?branch=main)
[![PyPI License](https://img.shields.io/pypi/l/verchew.svg)](https://pypi.org/project/verchew)
[![PyPI Version](https://img.shields.io/pypi/v/verchew.svg)](https://pypi.python.org/pypi/verchew)
[![PyPI Downloads](https://img.shields.io/pypi/dm/verchew.svg?color=orange)](https://pypistats.org/packages/verchew)

# Setup

## Requirements

- Python 2.7+ or Python 3.3+

## Installation

Install `verchew` globally with [pipx](https://pipxproject.github.io/pipx/installation/) (or pip):

```text
$ pipx install verchew
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add verchew
```

or embedded the script in your project using [this guide](https://verchew.readthedocs.io/en/latest/cli/vendoring/).

# Usage

Run `verchew --init` to generate a sample configuration file.

Update this file (`verchew.ini`) to include your project's system dependencies:

```ini
[Working Program]

cli = working-program
version = 1.2

[Newer Working Program]

cli = working-program
version =  4.1 || 4.2
message = Version 4.x is required to get the special features.

[Broken Program]

cli = broken-program
version = 1.2.3

[Optional Missing Program]

cli = missing-program
version = 1.2.3
optional = true

[Missing Program]

cli = missing-program
version = 1.2.3
```

Run `verchew` to see if you have the expected versions installed:

```text
$ verchew

Checking for Working Program...

$ working-program --version
1.2.3
✔ MATCHED: 1.2

Checking for Newer Working Program...

$ working-program --version
1.2.3
✘ EXPECTED: 4.1 || 4.2
䷉ MESSAGE: Version 4.x is required to get the special features.

Checking for Broken Program...

$ broken-program --version
An error occurred.
✘ EXPECTED: 1.2.3

Checking for Optional Missing Program...

$ missing-program --version
sh: command not found: missing-program
▴ EXPECTED (OPTIONAL): 1.2.3

Checking for Missing Program...

$ missing-program --version
sh: command not found: missing-program
✘ EXPECTED: 1.2.3

Results: ✔ ✘ ✘ ▴ ✘
```
