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

    async def inner_run(self, job_info):
        pass


class ImageFlowAPI(tornado.web.RequestHandler):
    def get(self):

        request = self.request
        params = json.loads(request.body)
        Logger.info("image flow api params: %s", params)

        result = add_a_request("job_image_flow", params)
        Logger.info(result)

        self.write(result)

    def post(self):
        self.get()


JOB_NAME = get_job_name(__file__)
ClassObj = JobImageFlow

API_NAME = "/image_flow"
APIClassObj = ImageFlowAPI
