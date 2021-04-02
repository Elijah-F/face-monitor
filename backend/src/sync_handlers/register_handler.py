#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web
from helpers import db_operator


class RegisterAPI(tornado.web.RequestHandler):
    def initialize(self):
        self.db_operator = db_operator.DbOperator()

    def post(self):
        data = json.loads(self.request.body)
        phone = data["phone"]
        result = {"code": 0, "message": "ok"}

        if self.phone_exists(phone):
            result["code"] = -1
            result["message"] = "Phone number has existed."
            self.write(result)
            return

        self.db_operator.insert_user_info(phone)
        self.write(result)

    def phone_exists(self, phone):
        rows = self.db_operator.select_user_info(phone)
        return len(rows) > 0


API_NAME = "/register"
APIClassObj = RegisterAPI
