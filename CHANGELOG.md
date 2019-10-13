# 2.0 (2019-10-13)

- Deprecated `versions` in favor of `version` option.
- Deprecated `|` in favor of `||` for checking multiple versions.
- Dropped support for Python 2, Python 3.4, and Python 3.5

# 1.6.3 (2019-10-12)

- Fixed handling of programs that produce no output.

# 1.6.2 (2019-02-15)

- Fixed handling of programs that produce output with file paths.

# 1.6.1 (2019-02-14)

- Fixed handling of programs that produce no output.

# 1.6 (2019-02-08)

- Added `--quiet` option to suppress output when all programs match.

# 1.5 (2018-12-24)

- Updated `version` to only match at word boundaries.

# 1.4 (2018-03-06)

- Updated `cli_version_arg` to be blank for programs with no version argument.

# 1.3 (2018-02-08)

- Added support for checking for multiple versions of programs.

# 1.2 (2017-09-13)

- Added `optional = true` settings to downgrade errors to warnings.
- Added `message` setting to display optional message for missing programs.

# 1.1 (2017-05-17)

- Added `--init` command to generate a sample configuration file.

# 1.0 (2017-01-09)

- Initial stable release.

# 0.5 (2016-11-02)

- Added `--exit-code` option to return non-zero exit codes on failure.

# 0.4 (2016-10-20)

- Added support for custom version arguments.
- Fixed handling of internal versions matches.

# 0.3 (2016-10-18)

- Added support for detecting missing and broken programs.

# 0.2.1 (2016-10-18)

- Now stripping whitespace after calling `--version` on a program.

# 0.2 (2016-10-17)

- Added `--version` command.

# 0.1 (2016-10-17)

 - Initial release.
