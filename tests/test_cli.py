# -*- coding: utf-8 -*-

# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

from __future__ import unicode_literals

import logging
import os
import sys

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
✔ MATCHED: 1.2

Checking for Newer Working Program...

$ working-program --version
1.2.3
✘ EXPECTED: 4.1 || 4.2
䷉ MESSAGE: Version 4.x is required to get the special features.

Checking for Broken Program...

$ broken-program --version
An error occurred.
✘ EXPECTED: 1.2.3

Checking for Optional Missing Program...

$ missing-program --version
sh: command not found: missing-program
▴ EXPECTED (OPTIONAL): 1.2.3

Checking for Missing Program...

$ missing-program --version
sh: command not found: missing-program
✘ EXPECTED: 1.2.3

Results: ✔ ✘ ✘ ▴ ✘

"""

UNSTYLED_OUTPUT = (
    STYLED_OUTPUT.replace("✔", "~")
    .replace("䷉", "#")
    .replace("▴", "?")
    .replace("✘", "x")
)

UNSTYLED_OUTPUT_WINDOWS = """
Checking for Working Program...

$ working-program --version
sh: command not found: working-program
x EXPECTED: 1.2

Checking for Newer Working Program...

$ working-program --version
sh: command not found: working-program
x EXPECTED: 4.1 || 4.2
# MESSAGE: Version 4.x is required to get the special features.

Checking for Broken Program...

$ broken-program --version
sh: command not found: broken-program
x EXPECTED: 1.2.3

Checking for Optional Missing Program...

$ missing-program --version
sh: command not found: missing-program
? EXPECTED (OPTIONAL): 1.2.3

Checking for Missing Program...

$ missing-program --version
sh: command not found: missing-program
x EXPECTED: 1.2.3

Results: x x x ? x

"""

log = logging.getLogger(__name__)


@pytest.fixture
def env(tmpdir):
    path = str(tmpdir.join("test"))
    env = scripttest.TestFileEnvironment(path)
    os.chdir(path)
    env.environ["PATH"] = BIN_DIR
    log.debug("ENV: %s", env.environ)
    return env


@pytest.fixture
def cli(env):
    path = os.path.join(os.path.dirname(sys.executable), "verchew")
    return lambda *args: call(env, path, *args)


def call(env, path, *args):
    log.info("$ %s %s", path, " ".join(args))
    return env.run(path, *args, expect_error=True)


def describe_meta():
    def it_displays_help_information(cli):
        cmd = cli("--help")

        expect(cmd.stdout).contains("usage: verchew")
        expect(cmd.returncode) == 0

    def it_displays_version_information(cli):
        cmd = cli("--version")

        expect(cmd.stdout).startswith("verchew v")
        expect(cmd.returncode) == 0


def describe_init():
    def it_generates_a_sample_config(cli):
        cmd = cli("--init")

        expect(cmd.stderr) == ""
        expect(cmd.stdout).contains("Checking for Make")
        expect(cmd.returncode) == 0


def describe_vendor():
    @pytest.mark.skipif(sys.platform == "win32", reason="unix only")
    def it_creates_a_new_file_on_unix(cli):
        cmd = cli("--vendor", "bin/verchew")

        expect(cmd.stderr) == ""
        expect(cmd.stdout) == ""
        expect(cmd.returncode) == 0
        expect(cmd.files_created).contains("bin/verchew")

    @pytest.mark.skipif(sys.platform != "win32", reason="windows only")
    def it_creates_a_new_file_on_windows(cli):
        cmd = cli("--vendor", "bin\\verchew")

        expect(cmd.stderr) == ""
        expect(cmd.stdout) == ""
        expect(cmd.returncode) == 0
        expect(cmd.files_created).contains("bin\\verchew")


def describe_main():
    @pytest.mark.skipif(
        sys.version_info[0] == 2 or sys.platform == "win32",
        reason="unix and python3 only",
    )
    def it_displays_results_on_unix_python_3(cli):
        cmd = cli("--root", EXAMPLES_DIR)

        expect(cmd.stderr) == ""
        expect(cmd.stdout) == STYLED_OUTPUT
        expect(cmd.returncode) == 0

    @pytest.mark.skipif(
        sys.version_info[0] == 3 or sys.platform == "win32",
        reason="unix and python2 only",
    )
    def it_displays_results_on_unix_python_2(cli):
        cmd = cli("--root", EXAMPLES_DIR)

        expect(cmd.stderr) == ""
        expect(cmd.stdout) == UNSTYLED_OUTPUT
        expect(cmd.returncode) == 0

    @pytest.mark.skipif(sys.platform != "win32", reason="windows only")
    def it_displays_results_on_windows(cli):
        cmd = cli("--root", EXAMPLES_DIR)

        expect(cmd.stderr) == ""
        expect(cmd.stdout) == UNSTYLED_OUTPUT_WINDOWS
        expect(cmd.returncode) == 0

    def it_exits_with_an_error_code_if_enabled(cli):
        cmd = cli("--root", EXAMPLES_DIR, "--exit-code")

        expect(cmd.returncode) == 1


def describe_quiet():
    @pytest.mark.skipif(sys.platform == "win32", reason="unix only")
    def it_hides_output_when_no_error(cli, tmp_path):
        verchew_ini = tmp_path / "verchew.ini"
        verchew_ini.write_text(
            """
        [Working Program]

        cli = working-program
        version = 1.2
        """
        )

        cmd = cli("--root", str(tmp_path), "--quiet")

        expect(cmd.stderr) == ""
        expect(cmd.stdout) == ""
        expect(cmd.returncode) == 0

    @pytest.mark.skipif(sys.platform == "win32", reason="unix only")
    def it_shows_failing_programs(cli, tmp_path):
        verchew_ini = tmp_path / "verchew.ini"
        verchew_ini.write_text(
            """
        [Working Program]

        cli = working-program
        version = 1.2

        [Newer Working Program]

        cli = working-program
        version =  1.3

        [Missing Program]

        cli = missing-program
        version = 1.2.3
        """
        )

        cmd = cli("--root", str(tmp_path), "--quiet")

        expect(cmd.stderr) == ""
        expect(cmd.stdout) == (
            "Newer Working Program: 1.2.3, EXPECTED: 1.3\n"
            "Missing Program: Not found, EXPECTED: 1.2.3\n"
        )
        expect(cmd.returncode) == 0
