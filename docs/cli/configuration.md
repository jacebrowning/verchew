# Filenames

Any of the following can be used as the `verchew` configuration filename:

* `.verchew.ini`
* `verchew.ini`
* `.verchew`
* `.verchewrc`
    
# Version Arguments

If one of your system dependencies using an argument other than `--version` to display its version information, this can be changed in the configuration file using the `cli_version_arg` setting:

```ini
[Graphviz]

cli = dot
cli_version_arg = -V
version = 2.
```

# Multiple Versions

If your project can use multiple versions of a system dependency, use the `versions` setting and separate versions with the pipe character (`|`):

```ini
[Python]

cli = python
versions = Python 2. | Python 3.
```

# Optional Programs

If one of your system dependencies is optional and you only want to show a warning for incompatible versions, include the `optional` setting:

```ini
[Terminal Notifier]

cli = terminal-notifier
version = 1.8
optional = true
```

# Help Messages

To provide additional information when a system dependency is missing, include the `message` setting:

```ini
[Git]

cli = git
version = 2.
message = Version 2.x is required to get the new push behavior.
```
