#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web
from common import Logger, get_job_name


class JobImageFlow:
    pass


class ImageFlowAPI(tornado.web.RequestHandler):
    def get(self):

        request = self.request
        params = json.loads(request.body)
        Logger.info("image flow api params: %s", params)

        # TODO:
        result = {"code": "ok"}
        Logger.info(result)

        self.write(json.dumps(result))

    def post(self):
        self.get()


JOB_NAME = get_job_name(__file__)
ClassObj = JobImageFlow

API_NAME = "/image_flow"
APIClassObj = ImageFlowAPI
