#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import tornado.web
from helpers import db_operator, room_pool

PhoneNotExist = {"code": -100, "message": "Phone number has not existed."}
RoomExist = {"code": 100, "message": "Room number has existed."}


class LoginAPI(tornado.web.RequestHandler):
    def initialize(self):
        self.db_operator = db_operator.DbOperator()
        self.rooms = room_pool.RoomPool()

    def post(self):
        data = json.loads(self.request.body)
        phone = data["phone"]
        room = data["room"]
        result = {"code": 0, "message": "ok"}

        # Does the acount exists?
        user_info = self.db_operator.select_user_info(phone)
        if len(user_info) == 0:
            result["code"] = PhoneNotExist["code"]
            result["message"] = PhoneNotExist["message"]
            self.write(result)
            return

        if room in self.rooms:
            result["code"] = RoomExist["code"]
            result["message"] = RoomExist["message"]

        result["name"] = "" if user_info[0]["name"] is None else user_info[0]["name"]
        self.write(result)


API_NAME = "/login"
APIClassObj = LoginAPI
