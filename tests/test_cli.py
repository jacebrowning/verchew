# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

from __future__ import unicode_literals

import os
import sys

import pytest
import scripttest
from expecter import expect
import six


@pytest.fixture
def env(tmpdir):
    path = str(tmpdir.join('test'))
    env = scripttest.TestFileEnvironment(path)
    return env


def cli(env, *args):
    prog = os.path.join(os.path.dirname(sys.executable), 'verchew')
    cmd = env.run(prog, *args, expect_error=True)
    six.print_(cmd)
    return cmd


def describe_cli():

    def it_displays_help_information(env):
        cmd = cli(env, '--help')

        expect(cmd.returncode) == 0
        expect(cmd.stdout).contains("usage: verchew")

    def it_displays_version_information(env):
        cmd = cli(env, '--version')

        expect(cmd.returncode) == 0
        expect(cmd.stdout or cmd.stderr).contains("verchew v0.")
