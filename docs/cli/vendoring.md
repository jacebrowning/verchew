# Standalone Script

Normally, `verchew` is installed using `pip`, but given the variety of environments in which this program is run, you might be in a situation where `pip`:

* is not installed
* does not have the correct permissions to install `verchew`
* does not have network access to PyPI

For this reason, `verchew` can also be embedded into your project as a standalone Python script.

## Building

After cloning this repository, build the script for distribution:

```
$ make dist
```

## Copying

In your project:

1. Create a `bin/` directory: `$ mkdir -p bin`
2. Copy the script: `$ cp ../verchew/dist/verchew bin/verchew`
3. Ensure the script is executable: `$ chmod a+x bin/verchew`

An example of this can be seen [here](https://github.com/jacebrowning/template-python-demo).
