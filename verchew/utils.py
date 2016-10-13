import sys
import logging


log = logging.getLogger(__name__)


def display(text):
    sys.stdout.write(text + '\n')
