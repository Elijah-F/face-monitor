#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import threading
import traceback
import uuid

from base_task import BaseTask
from common import Logger, init_logger
from handler_container import HandlerContainer, import_handler


class JobMgr(BaseTask):
    def __init__(self, loop):
        super().__init__(loop, init_logger("job_mgr"))
        self._job_queue = asyncio.Queue(maxsize=1000, loop=self._loop)
        self._handler_ctn = HandlerContainer()

    async def inner_run(self, data=None):
        _ = data
        self._logger.info("JobMgr start")

        while True:
            try:
                job_info = await self._job_queue.get()

                handler_name = job_info["handler_name"]
                handler_type = self._handler_ctn.get_handler(handler_name)
                if not handler_type:
                    self._logger.warning("handler_name key error")
                    continue

                logger = init_logger(handler_name)
                obj = handler_type(self._loop, logger)

                self._loop.create_task(obj.start(job_info))
                self._logger.info("create a new job %s", job_info["job_id"])

            except Exception:  # pylint: disable=broad-except
                self._logger.error(traceback.format_exc())

    async def add_job(self, job_info):
        await self._job_queue.put(job_info)
        self._logger.info("new request query: %s", job_info)

    def add_job_threadsafe(self, job_info):
        asyncio.run_coroutine_threadsafe(self.add_job(job_info), self._loop)


_JOBMGR = None


def add_a_request(handler_name, params):
    global _JOBMGR

    job_id = str(uuid.uuid1())
    job_info = dict()
    job_info["handler_name"] = handler_name
    job_info["job_id"] = job_id
    job_info["params"] = params
    Logger.info("new request query: %s", job_info)

    _JOBMGR.add_job_threadsafe(job_info)

    result = {"code": 0, "msg": "ok", "job_id": job_id}
    Logger.info("new request result: %s", result)

    return result


def _event_loop():
    global _JOBMGR

    # print msg into console
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(True)

    _JOBMGR = JobMgr(loop)
    loop.create_task(_JOBMGR.start())

    loop.run_forever()
    loop.close()
    Logger.info("JobMgr done")


def start_job_mgr():
    import_handler("./sync_handlers")
    import_handler("./async_handlers")

    thd = threading.Thread(target=_event_loop)
    thd.start()
    Logger.info("JobMgr start")
