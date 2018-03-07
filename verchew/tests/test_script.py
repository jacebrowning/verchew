# -*- coding: utf-8 -*-

# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

from __future__ import unicode_literals

import pytest
from expecter import expect

from verchew.script import (find_config, parse_config, get_version,
                            match_version, _)


def write(config, text, indent=8):
    config.write(text.replace(' ' * indent, ''))


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
        write(config, """
        [Foobar]
        """)

        expect(parse_config(str(config))) == {
            'Foobar': {
                'versions': '',
                'patterns': [''],
            },
        }

    def with_a_filled_section(config):
        write(config, """
        [Foobar]

        cli = foobar
        version = v1.2.3
        """)

        expect(parse_config(str(config))) == {
            'Foobar': {
                'cli': 'foobar',
                'versions': 'v1.2.3',
                'patterns': ['v1.2.3'],
            },
        }

    def with_multiple_versions(config):
        write(config, """
        [Foobar]

        version = 1
        versions = 2 | 3 |     4
        """)

        expect(parse_config(str(config))) == {
            'Foobar': {
                'versions': '2 | 3 |     4',
                'patterns': ['2', '3', '4'],
            },
        }


def describe_get_version():

    def when_missing():
        expect(get_version('foobar')) == "sh: command not found: foobar"

    def when_found():
        expect(get_version('python')).contains("Python ")

    def with_custom_argument():
        expect(get_version('python', argument='-V')).contains("Python ")

    def with_no_argument():
        expect(get_version('pip', argument='')).contains("Usage:")


def describe_match_version():

    def when_exact():
        expect(match_version("1.2.3", "1.2.3")) == True

    def when_partial():
        expect(match_version("1.2.", "1.2.3")) == True

    def when_mismatch():
        expect(match_version("1.", "2.0")) == False

    def when_match_inside():
        expect(match_version("1.", "Foobar 1.2.3")) == True

    def when_mismatch_inside():
        expect(match_version("2.", "Foobar 1.2.3")) == False


def describe_format():

    def default():
        expect(_('~')) == "~"

    @pytest.mark.parametrize("is_tty,supports_utf8,supports_ansi,formatted", [
        (0, 0, 0, "~"),
        (0, 0, 1, "~"),
        (0, 1, 0, "✔"),
        (0, 1, 1, "✔"),
        (1, 0, 0, "~"),
        (1, 0, 1, "\033[92m~\033[0m"),
        (1, 1, 0, "✔"),
        (1, 1, 1, "\033[92m✔\033[0m"),
    ])
    def with_options(is_tty, supports_utf8, supports_ansi, formatted):
        options = dict(is_tty=is_tty,
                       supports_utf8=supports_utf8,
                       supports_ansi=supports_ansi)

        expect(_('~', **options)) == formatted
