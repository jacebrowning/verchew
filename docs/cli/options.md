# Configuration Generation

In a new project, a sample configuration file can be generated:

```sh
$ verchew --init
```

Update the generated file to match your project's system dependencies, including an optional `message` where helpful.

# Custom Project Root

To call `verchew` from an arbitrary directory, pass it the path to the root of your project:

```sh
$ verchew --root=<path/to/project>
```

# Exit Codes

When `verchew` runs, it will always return an exit code of 0 to avoid interrupting continuous integration. To force a non-zero exit code on failure, use the `--exit-code` option:

```sh
$ verchew --exit-code
```
