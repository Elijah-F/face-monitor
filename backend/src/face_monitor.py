#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import common
import daemon
import job_mgr
import webapp


def main(run_as_daemon=False):
    if run_as_daemon:
        daemon.run_as_daemon()

    # change work dir from 'face_monitor' to 'face_monitor/backend/src'
    common.change_dir()

    # job mgr
    job_mgr.start_job_mgr()

    # webapp
    webapp.start_webapp()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        main(True)
    else:
        main(False)
