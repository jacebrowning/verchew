"""Sample integration test module."""
# pylint: disable=no-self-use,missing-docstring

import unittest

from click.testing import CliRunner

from verchew.script import main


class TestVerchew(unittest.TestCase):
    """Sample integration test class."""

    def test_conversion(self):
        runner = CliRunner()
        result = runner.invoke(main, [])

        self.assertEqual(result.exit_code, -1)
