#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import argparse
try:
    import configparser  # Python 3
except ImportError:
    import ConfigParser as configparser  # Python 2
import subprocess
import logging


CONFIG_FILENAMES = ['.verchew', '.verchewrc', 'verchew.ini', '.verchew.ini']

log = logging.getLogger(__name__)


def main():
    args = parse_args()
    configure_logging(args.verbose)
    path = find_config()
    config = parse_config(path)
    if not check_dependencies(config):
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    # TODO: add '--version' option
    # parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="enable verbose logging")

    return parser.parse_args()


def configure_logging(count=0):
    if count == 0:
        level = logging.WARNING
    elif count == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def find_config(root=None, config_filenames=None):
    root = root or os.getcwd()
    config_filenames = config_filenames or CONFIG_FILENAMES

    path = None
    log.info("Looking for config file in: %s", root)
    log.debug("Filename options: %s", ", ".join(config_filenames))
    for filename in os.listdir(root):
        if filename in config_filenames:
            path = os.path.join(root, filename)
            log.info("Found config file: %s", path)
            return path

    msg = "No config file found in: {0}".format(root)
    raise RuntimeError(msg)


def parse_config(path):
    data = {}

    log.info("Parsing config file: %s", path)
    config = configparser.ConfigParser()
    config.read(path)

    for section in config.sections():
        data[section] = {}
        for name, value in config.items(section):
            data[section][name] = value

    return data


def check_dependencies(config):
    success = []

    for name, settings in config.items():
        show("Checking for {0}...".format(name), head=True)
        output = get_version(settings['cli'])
        if settings['version'] in output:
            show("✔ MATCHED: {0}".format(settings['version']))
            success.append("✔")
        else:
            show("✖ EXPECTED: {0}".format(settings['version']))
            success.append("✖")

    show("Results: " + " ".join(success), head=True)

    return "✖" not in success


def get_version(program):
    args = [program, '--version']

    show("$ {0}".format(" ".join(args)))
    try:
        raw = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except OSError:
        output = "command not found"
    else:
        output = raw.decode('utf-8')
    log.debug("Command output: %r", output)

    show(output.splitlines()[0])

    return output


def show(text, start='', end='\n', head=False):
    """Python 2 and 3 compatible version of print."""
    if head:
        start = '\n'
        end = '\n\n'

    if log.getEffectiveLevel() < logging.WARNING:
        log.info(text)
    else:
        sys.stdout.write(start + text + end)


if __name__ == '__main__':  # pragma: no cover
    main()
