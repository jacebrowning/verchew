# Filenames

Any of the following can be used as the `verchew` configuration filename:

- `.verchew.ini`
- `verchew.ini`
- `.verchew`
- `.verchewrc`

# Version Arguments

If one of your system dependencies uses an argument other than `--version` to display its version information, this can be changed in the configuration file using the `cli_version_arg` setting:

```ini
[Graphviz]

cli = dot
cli_version_arg = -V
version = 2
```

To pass multiple args, use spaces as separators.

If the program lacks a specific argument to display its version, but contains version information in the default output, include an empty `cli_version_arg` setting:

```ini
[7-Zip]

cli = 7z
cli_version_arg =
version = 16
```

# Multiple Versions

If your project can work with more than one version of a system dependency, separate them with a double pipe (`||`) symbol:

```ini
[Python]

cli = python
version = Python 2 || Python 3
```

# Any Version

If the version of a system dependency is not important to your project, leave out the `version` setting to simply check for the existence of that program:

```ini
[Hugo]

cli = hugo
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
version = 2
message = Version 2.x is required to get the new push behavior.
```
