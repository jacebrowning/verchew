# -*- coding: utf-8 -*-

# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

from __future__ import unicode_literals

import os
import sys
import logging

import pytest
import scripttest
from expecter import expect

TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.join(TESTS_DIR, "..")
EXAMPLES_DIR = os.path.join(ROOT_DIR, "examples")
BIN_DIR = os.path.join(EXAMPLES_DIR, "bin")

STYLED_OUTPUT = """
Checking for Working Program...

$ working-program --version
1.2.3
✔ MATCHED: 1.2.

Checking for Newer Working Program...

$ working-program --version
1.2.3
✘ EXPECTED: 4.

Checking for Broken Program...

$ broken-program --version
An error occurred.
✘ EXPECTED: 1.2.3

Checking for Missing Program...

$ missing-program --version
sh: command not found: missing-program
✘ EXPECTED: 1.2.3

Results: ✔ ✘ ✘ ✘

"""

UNSTYLED_OUTPUT = STYLED_OUTPUT.replace('✔', '~').replace('✘', 'x')

UNSTYLED_OUTPUT_WINDOWS = """
Checking for Working Program...

$ working-program --version
sh: command not found: working-program
x EXPECTED: 1.2.

Checking for Newer Working Program...

$ working-program --version
sh: command not found: working-program
x EXPECTED: 4.

Checking for Broken Program...

$ broken-program --version
sh: command not found: broken-program
x EXPECTED: 1.2.3

Checking for Missing Program...

$ missing-program --version
sh: command not found: missing-program
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
    env.environ['PATH'] = BIN_DIR
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
        cmd = cli(env_with_bin, '--root', EXAMPLES_DIR)

        expect(cmd.returncode) == 1
        expect(cmd.stderr) == ""
        expect(cmd.stdout) == STYLED_OUTPUT

    @pytest.mark.skipif(sys.platform == 'win32', reason="unix-only")
    @pytest.mark.skipif(sys.version_info[0] == 3, reason="python2-only")
    def it_displays_results_on_unix_python_2(env_with_bin):
        cmd = cli(env_with_bin, '--root', EXAMPLES_DIR)

        expect(cmd.returncode) == 1
        expect(cmd.stderr) == ""
        expect(cmd.stdout) == UNSTYLED_OUTPUT

    @pytest.mark.skipif(sys.platform != 'win32', reason="windows-only")
    def it_displays_results_on_windows(env_with_bin):
        cmd = cli(env_with_bin, '--root', EXAMPLES_DIR)

        expect(cmd.returncode) == 1
        expect(cmd.stderr) == ""
        expect(cmd.stdout) == UNSTYLED_OUTPUT_WINDOWS
