#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web
from base_task import BaseTask
from common import Logger, get_job_name
from job_mgr import add_a_request


class JobImageFlow(BaseTask):
    def __init__(self, loop, logger):
        super().__init__(loop, logger)
        self._params = None
        self._job_id = None

    async def inner_run(self, job_info):
        await self.parse_job_info(job_info)
        print(self._job_id)

    async def parse_job_info(self, job_info):
        self._params = job_info["params"]
        self._job_id = job_info["job_id"]


class ImageFlowAPI(tornado.web.RequestHandler):
    def get(self):

        request = self.request
        params = json.loads(request.body)
        Logger.info("image flow api params: %s", params)

        result = add_a_request(JOB_NAME, params)
        Logger.info(result)

        self.write(result)

    def options(self):
        self.get()


JOB_NAME = get_job_name(__file__)
ClassObj = JobImageFlow

API_NAME = "/image_flow"
APIClassObj = ImageFlowAPI
