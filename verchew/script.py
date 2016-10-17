import os
import argparse
import logging


CONFIG_FILENAMES = ['.verchew', '.verchewrc', 'verchew.ini', '.verchew.ini']


log = logging.getLogger(__name__)


def main():
    args = parse_arguments()
    configure_logging(args.verbose)
    find_config()


def parse_arguments():
    parser = argparse.ArgumentParser()
    # TODO: add '--version' option
    # parser.add_argument('-V', '--version', action='version', version=VERSION)
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


if __name__ == '__main__':  # pragma: no cover
    main()
