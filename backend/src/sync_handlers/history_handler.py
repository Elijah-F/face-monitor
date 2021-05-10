#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tornado.web
from helpers import db_operator


class HistoryAPI(tornado.web.RequestHandler):
    db_operator = db_operator.DbOperator()

    def get(self):
        phone = self.get_query_argument("phone")

        rows = self.db_operator.select_history(phone)

        self.write("hello world")


API_NAME = "/history"
APIClassObj = HistoryAPI
