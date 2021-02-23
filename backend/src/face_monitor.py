#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from . import daemon


def main(run_as_daemon=False):
    if run_as_daemon:
        daemon.run_as_daemon()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        main(True)
    else:
        main(False)
