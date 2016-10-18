# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

from __future__ import unicode_literals

import os
import sys

import pytest
import scripttest
from expecter import expect


ROOT = os.path.abspath(os.path.dirname(__file__))
FILES = os.path.join(ROOT, "files")
BIN = os.path.join(FILES, "bin")

SAMPLE_OUTPUT = """
Checking for Valid Program...

$ working --version
1.2.3
✔ MATCHED: 1.2.

Checking for Invalid Program...

$ working --version
1.2.3
✖ EXPECTED: 4.

Checking for Broken Program...

$ broken --version
An error occurred.
✖ EXPECTED: 1.2.3

Checking for Missing Program...

$ missing --version
sh: command not found: missing
✖ EXPECTED: 1.2.3

Results: ✔ ✖ ✖ ✖

"""


@pytest.fixture
def env(tmpdir):
    path = str(tmpdir.join("test"))
    env = scripttest.TestFileEnvironment(path)
    return env


def cli(env, *args):
    prog = os.path.join(os.path.dirname(sys.executable), "verchew")
    cmd = env.run(prog, *args, expect_error=True)
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

    def it_displays_results_when_run(env):
        env.environ['PATH'] = BIN
        cmd = cli(env, '--root', FILES)

        expect(cmd.returncode) == 1
        expect(cmd.stdout) == SAMPLE_OUTPUT
