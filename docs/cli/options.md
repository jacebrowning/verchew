# Configuration Filenames

Any of the following can be used as the `verchew` configuration filename:

* `.verchew`
* `.verchewrc`
* `verchew.ini`
* `.verchew.ini`

# Custom Project Root

To call `verchew` from an arbitrary directory, pass it the path to the root of your project:

```sh
$ verchew --root=<path/to/project>
```

# Custom Version Arguments

If one of your system dependencies using an argument other than `--version` to display its version information, this can be changed in the configuration file using the `cli_version_arg` setting:

```ini

[Graphviz]

cli = dot
cli_version_arg = -V

version = 2.

```
