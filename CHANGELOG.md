# 4.0 (beta)

- Updated script to assume `python3` is available, dropping support for legacy Python.

# 3.2.1 (2022-01-12)

- Fix handling of `optional=false` in configuration files.

# 3.2 (2022-01-07)

- Added support for passing multiple version arguments.

# 3.1 (2020-04-18)

- Added support for unicode characters in Python 3.8.
- Added `--vendor PATH` command to download the program for offline use.
- Updated `--quiet` output to include actual program versions.

# 3.0.2 (2020-01-06)

- Removed type annotations to continue supporting legacy Python.

# 3.0.1 (2019-12-13)

- Fixed missing program detection to only look for "not found" in the first line.

# 3.0 (2019-12-07)

- Removed `versions` in favor of `version` option.
- Removed `|` in favor of `||` for checking multiple versions.
- Added support for matching **any** version when `version` is not specified.

# 2.0.1 (2019-10-13)

- Restore compatibility layer to unofficially support legacy Python.

# 2.0 (2019-10-13)

- Deprecated `versions` in favor of `version` option.
- Deprecated `|` in favor of `||` for checking multiple versions.
- Stopped testing against Python 2, Python 3.4, and Python 3.5.

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
