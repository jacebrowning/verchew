# -*- coding: utf-8 -*-

# pylint: disable=unused-variable,unused-argument,expression-not-assigned

from __future__ import unicode_literals

import pytest
from expecter import expect

from verchew.script import find_config, parse_config, get_version, _


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

    def when_found(config):
        path = find_config(config_filenames=["foo.bar"])

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
        config.write("""
        [Foobar]
        """.replace(' ' * 8, ''))

        expect(parse_config(str(config))) == {
            'Foobar': {},
        }

    def with_a_filled_section(config):
        config.write("""
        [Foobar]

        cli = foobar
        version = v1.2.3
        """.replace(' ' * 8, ''))

        expect(parse_config(str(config))) == {
            'Foobar': {
                'cli': 'foobar',
                'version': 'v1.2.3',
            },
        }


def describe_get_version():

    def when_missing():
        expect(get_version('foobar')) == "sh: command not found: foobar"

    def when_found():
        expect(get_version('python')).contains("Python ")

    def with_custom_argument():
        expect(get_version('python', argument='-V')).contains("Python ")


def describe_format():

    def when_utf8():
        expect(_('~', utf8=True)) == "✔"

    def when_tty():
        expect(_('~', tty=True)) == "\033[92m~\033[0m"

    def when_utf8_and_tty():
        expect(_('~', utf8=True, tty=True)) == "\033[92m✔\033[0m"
