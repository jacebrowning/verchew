# -*- coding: utf-8 -*-

# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison,use-implicit-booleaness-not-comparison

from __future__ import unicode_literals

import os

import pytest
from expecter import expect

from verchew.script import (
    SCRIPT_URL,
    _,
    find_config,
    get_version,
    match_version,
    parse_config,
    vendor_script,
)


def write(config, text, indent=8):
    config.write(text.replace(" " * indent, ""))


def describe_vendor_script():
    def when_missing_file(tmpdir):
        tmpdir.chdir()
        path = os.path.join(tmpdir, "missing")

        vendor_script(SCRIPT_URL, "missing")

        expect(os.access(path, os.X_OK)) == True
        with open(path, "r") as f:
            expect(f.read()).contains("verchew")

    def when_missing_directory(tmpdir):
        tmpdir.chdir()
        path = os.path.join(tmpdir, "bin/missing")

        vendor_script(SCRIPT_URL, "bin/missing")

        expect(os.access(path, os.X_OK)) == True
        with open(path, "r") as f:
            expect(f.read()).contains("verchew")

    def when_existing_file(tmpdir):
        tmpdir.chdir()
        path = os.path.join(tmpdir, "existing")
        with open(path, "w") as f:
            f.write("Hello, world!")

        vendor_script(SCRIPT_URL, "existing")

        expect(os.access(path, os.X_OK)) == True
        with open(path, "r") as f:
            expect(f.read()).contains("verchew")


def describe_find_config():
    @pytest.fixture
    def config(tmpdir):
        tmpdir.chdir()
        path = tmpdir.join("foo.bar")
        path.write("")
        return path

    def when_missing(config):
        with expect.raises(RuntimeError):
            find_config()

    def when_missing_and_generate(config):
        path = find_config(generate=True)

        generated_path = str(config).replace("foo.bar", "verchew.ini")
        expect(path) == generated_path

    def when_found(config):
        path = find_config(filenames=["foo.bar"])

        expect(path) == config


def describe_parse_config():
    @pytest.fixture
    def config(tmpdir):
        tmpdir.chdir()
        path = tmpdir.join("verchew.ini")
        path.write("")
        return path

    def with_no_content(config):
        config.write("")

        expect(parse_config(str(config))) == {}

    def with_an_empty_section(config):
        write(
            config,
            """
        [Foobar]
        """,
        )

        expect(parse_config(str(config))) == {
            "Foobar": {"version": "", "patterns": [""], "optional": False}
        }

    def with_a_filled_section(config):
        write(
            config,
            """
        [Foobar]

        cli = foobar
        version = v1.2.3
        optional = true
        """,
        )

        expect(parse_config(str(config))) == {
            "Foobar": {
                "cli": "foobar",
                "version": "v1.2.3",
                "patterns": ["v1.2.3"],
                "optional": True,
            }
        }

    def with_multiple_versions(config):
        write(
            config,
            """
        [Foobar]

        version = 2 || 3 ||     4
        """,
        )

        expect(parse_config(str(config))) == {
            "Foobar": {
                "version": "2 || 3 ||     4",
                "patterns": ["2", "3", "4"],
                "optional": False,
            }
        }


def describe_get_version():
    def when_missing():
        expect(get_version("foobar")) == "sh: command not found: foobar"

    def when_found():
        expect(get_version("python")).contains("Python ")

    def with_custom_argument():
        expect(get_version("python", argument="-V")).contains("Python ")

    def with_multiple_arguments():
        expect(get_version("python", argument="-V -V")).contains("Python ")

    def with_no_argument():
        expect(get_version("pip", argument="")).contains("Usage:")

    def when_no_output():
        expect(get_version("echo", argument="")) == ""


def describe_match_version():
    def when_exact_match():
        expect(match_version("1.2.3", "1.2.3")) == True

    def when_partial_match():
        expect(match_version("1.2.", "1.2.3")) == True

    def when_partial_match_at_boundary():
        expect(match_version("1.2", "1.2.3")) == True

    def when_mismatch():
        expect(match_version("1.", "2.0")) == False

    def when_mismatch_at_boundary():
        expect(match_version("1.2", "1.23")) == False

    def when_match_with_name():
        expect(match_version("1.", "Foobar 1.2.3")) == True

    def when_mismatch_with_name():
        expect(match_version("2.", "Foobar 1.2.3")) == False

    def when_match_with_version():
        expect(match_version("1.", "v1.2.3")) == True

    def when_mismatch_with_version():
        expect(match_version("2.", "v1.2.3")) == False

    def when_match_with_dash_followed_by_path():
        """Test that the output of `$ printenv DIRENV_DIR` can be matched."""
        expect(match_version("-", "-/foo/bar")) == True

    def when_match_with_slug_inside_path():
        """Test that the output of `$ which python` (pyenv) can be matched."""
        expect(
            match_version(".pyenv", "Users/foobar/.pyenv/versions/2.7.14/bin/python")
        ) == True

    def when_mismatch_with_missing_program():
        expect(match_version("", "program not found")) == False
        expect(match_version("", "v1.2.3\nother not found")) == True

    def when_mismatch_with_missing_program_from_asdf():
        expect(
            match_version("1.4.2", "No poetry executable found for poetry 1.4.2")
        ) == False

    def when_match_with_multiple_lines():
        expect(match_version("1.2", "Foobar\nVersion 1.2.3")) == True

    def when_mismatch_with_no_output():
        expect(match_version("1.2.3", "")) == False


def describe_format():
    @pytest.mark.parametrize(
        "is_tty,supports_utf8,supports_ansi,formatted",
        [
            (0, 0, 0, "~"),
            (0, 0, 1, "~"),
            (0, 1, 0, "✔"),
            (0, 1, 1, "✔"),
            (1, 0, 0, "~"),
            (1, 0, 1, "\033[92m~\033[0m"),
            (1, 1, 0, "✔"),
            (1, 1, 1, "\033[92m✔\033[0m"),
        ],
    )
    def with_options(is_tty, supports_utf8, supports_ansi, formatted):
        options = dict(
            is_tty=is_tty, supports_utf8=supports_utf8, supports_ansi=supports_ansi
        )

        expect(_("~", **options)) == formatted
