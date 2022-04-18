# Vendoring

Normally, `verchew` is installed using `pip`, but given the variety of environments in which this program is run, you might be in a situation where `pip`:

- is not installed
- does not have the correct permissions to install `verchew`
- does not have network access to PyPI

For this reason, `verchew` can also be embedded into your project as a standalone Python script.

## Setup

### Manual

Create a `bin/` directory in your project:

```
$ mkdir -p bin
```

Download the standalone script:

```
$ wget https://raw.githubusercontent.com/jacebrowning/verchew/main/verchew/script.py
$ mv script.py bin/verchew
```

Ensure the script has executable permissions:

```
$ chmod a+x bin/verchew
```

### Automatic

If you already have `verchew` installed, it can download itself:

```
$ verchew --vendor bin/verchew
```

This will also create a `verchew-wrapper` script, which attempts to locate `python` on operating systems not compliant with [PEP 394](https://peps.python.org/pep-0394/), such as newer versions of macOS.

## Usage

To check the versions of your system dependencies simply run:

```
$ bin/verchew
```

An example of a project configured this way can be found [here](https://github.com/jacebrowning/template-python-demo).
