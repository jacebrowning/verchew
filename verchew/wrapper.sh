#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# See `verchew` for licensing and documentation links.

set -e
set -o pipefail

python3 script.py "$@"
