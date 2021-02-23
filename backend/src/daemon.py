#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys


def run_as_daemon():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        print("fork error! {}".format(err.strerror))
        sys.exit(-1)

    # Appoint the child process as the new session leader and process leader
    os.setsid()
    os.umask(0)
