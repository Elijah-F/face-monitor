#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
from helpers import db_operator


class ImageHistoryAPI(tornado.web.RequestHandler):
    db_operator = db_operator.DbOperator()

    def get(self):
        job_id = self.get_query_argument("job_id")
        rows = self.db_operator.select_image_history(job_id)

        data = {"smile": list(), "face": list(), "sleepy": list(), "speak": list()}
        for row in rows:
            data[row["type"]].append(row["image_data"])

        self.write(data)


API_NAME = "/image_history"
APIClassObj = ImageHistoryAPI
