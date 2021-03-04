#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
from base_task import BaseTask
from common import Logger, get_job_name
from job_mgr import add_a_request


class JobImageFlow(BaseTask):
    def __init__(self, loop, logger):
        super().__init__(loop, logger)
        self._image = None
        self._job_id = None

    async def inner_run(self, job_info):
        await self.parse_job_info(job_info)

        self._logger.info("job_image_flow inner_run: %s", self._job_id)

        # save image into cache dir
        with open("/".join(["../cache", self._image["filename"]]), "wb") as img:
            img.write(self._image["body"])

    async def parse_job_info(self, job_info):
        self._image = job_info["params"]
        self._job_id = job_info["job_id"]


class ImageFlowAPI(tornado.web.RequestHandler):
    def post(self):
        image = self.request.files["image"][0]
        Logger.info("new post request image: %s %s", image["filename"], image["content_type"])

        result = add_a_request(JOB_NAME, image)
        self.write(result)


JOB_NAME = get_job_name(__file__)
ClassObj = JobImageFlow

API_NAME = "/image_flow"
APIClassObj = ImageFlowAPI
