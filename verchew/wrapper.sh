#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# See `verchew` for licensing and documentation links.

set -e
set -o pipefail

if [ -e verchew ]
then
    python3 verchew "$@"
else
    python3 script.py "$@"
fi
