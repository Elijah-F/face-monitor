#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
from helpers import db_operator


class LoginAPI(tornado.web.RequestHandler):
    def initialize(self):
        self.db_operator = db_operator.DbOperator()

    def post(self):
        phone = self.get_body_argument("phone")
        result = {"success": 0, "message": "ok"}

        user_info = self.db_operator.select_user_info(phone)
        if len(user_info) == 0:
            result["success"] = -1
            result["message"] = "Phone number has not existed."
            self.write(result)
            return

        result["name"] = "" if user_info[0]["name"] is None else user_info[0]["name"]
        self.write(result)


API_NAME = "/login"
APIClassObj = LoginAPI
