# pylint: disable=unused-variable,unused-argument,expression-not-assigned

import pytest
from expecter import expect

from verchew.script import find_config


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
