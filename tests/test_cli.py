# -*- coding: utf-8 -*-

# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

from __future__ import unicode_literals

import os
import sys
import logging

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

SAMPLE_OUTPUT_PYTHON_2 = """
Checking for Valid Program...

$ working --version
1.2.3
~ MATCHED: 1.2.

Checking for Invalid Program...

$ working --version
1.2.3
x EXPECTED: 4.

Checking for Broken Program...

$ broken --version
An error occurred.
x EXPECTED: 1.2.3

Checking for Missing Program...

$ missing --version
sh: command not found: missing
x EXPECTED: 1.2.3

Results: ~ x x x

"""

SAMPLE_OUTPUT_WINDOWS = """
Checking for Valid Program...

$ working --version
sh: command not found: working
x EXPECTED: 1.2.

Checking for Invalid Program...

$ working --version
sh: command not found: working
x EXPECTED: 4.

Checking for Broken Program...

$ broken --version
sh: command not found: broken
x EXPECTED: 1.2.3

Checking for Missing Program...

$ missing --version
sh: command not found: missing
x EXPECTED: 1.2.3

Results: x x x x

"""

log = logging.getLogger(__name__)


@pytest.fixture
def env(tmpdir):
    path = str(tmpdir.join("test"))
    env = scripttest.TestFileEnvironment(path)
    return env


@pytest.fixture
def env_with_bin(env):
    env.environ['PATH'] = BIN
    log.debug("ENV: %s", env.environ)
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

    @pytest.mark.skipif(sys.platform == 'win32', reason="unix-only")
    @pytest.mark.skipif(sys.version_info[0] == 2, reason="python3-only")
    def it_displays_results_on_unix_python_3(env_with_bin):
        cmd = cli(env_with_bin, '--root', FILES)

        expect(cmd.returncode) == 1
        expect(cmd.stderr) == ""
        expect(cmd.stdout) == SAMPLE_OUTPUT

    @pytest.mark.skipif(sys.platform == 'win32', reason="unix-only")
    @pytest.mark.skipif(sys.version_info[0] == 3, reason="python2-only")
    def it_displays_results_on_unix_python_2(env_with_bin):
        cmd = cli(env_with_bin, '--root', FILES)

        expect(cmd.returncode) == 1
        expect(cmd.stderr) == ""
        expect(cmd.stdout) == SAMPLE_OUTPUT_PYTHON_2

    @pytest.mark.skipif(sys.platform != 'win32', reason="windows-only")
    def it_displays_results_on_windows(env_with_bin):
        cmd = cli(env_with_bin, '--root', FILES)

        expect(cmd.returncode) == 1
        expect(cmd.stderr) == ""
        expect(cmd.stdout) == SAMPLE_OUTPUT_WINDOWS
