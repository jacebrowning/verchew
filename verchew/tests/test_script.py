# pylint: disable=unused-variable,unused-argument,expression-not-assigned

import pytest
from expecter import expect

from verchew.script import find_config, parse_config, get_version


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
        """)

        expect(parse_config(str(config))) == {
            'Foobar': {},
        }

    def with_a_filled_section(config):
        config.write("""
        [Foobar]

        cli = foobar
        version = v1.2.3
        """)

        expect(parse_config(str(config))) == {
            'Foobar': {
                'cli': 'foobar',
                'version': 'v1.2.3',
            },
        }


def describe_get_version():

    def when_missing():
        expect(get_version('foobar')) == "command not found"

    def when_found():
        expect(get_version('python')).contains("Python ")
