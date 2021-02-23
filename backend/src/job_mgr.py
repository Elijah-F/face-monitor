#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

from .base_task import BaseTask
from .common import init_logger
from .handler_container import HandlerContainer


class JobMgr(BaseTask):
    def __init__(self, loop):
        super().__init__(loop, init_logger("job_mgr"))
        self._job_queue = asyncio.Queue(maxsize=1000, loop=self._loop)
        self._handler_ctn = HandlerContainer()

    async def inner_run(self, data=None):
        pass

    async def check_jobs(self):
        pass

    async def add_job(self, job_info):
        pass

    async def add_job_threadsafe(self, job_info):
        pass


_JobMgr = None


def event_loop():
    pass


def start_job_mgr():
    pass
