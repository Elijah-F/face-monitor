#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import uuid

import common
import tornado.websocket
from helpers import db_operator, face_helper, room_pool, utils


class RealTimeAPI(tornado.websocket.WebSocketHandler):
    logger = common.init_logger("real_time")
    face = face_helper.FaceHelper()
    rooms = room_pool.RoomPool()
    db_operator = db_operator.DbOperator()

    def check_origin(self, origin):
        allowed = ["http://192.168.12.133:8998"]
        if origin not in allowed:
            self.logger.info("not allowed origin %s", origin)
            return False
        return True

    def open(self, *args, **kwargs):
        self.phone = self.get_query_argument("phone")
        self.room = self.get_query_argument("room")

        if self.room not in self.rooms:
            # create a new room
            self.rooms[self.room]["admin"] = self.phone
            self.rooms[self.room]["unique_id"] = uuid.uuid1()

        self.rooms[self.room]["members"].append(self.phone)
        self.logger.info("new websocket opened.")

    def on_close(self):
        # if admin exit from room first, others exit from room will come error as room is not existed.
        # this `if` solve the problem above.
        if self.room in self.rooms:
            if self.phone == self.rooms[self.room]["admin"]:
                # admin close the room
                del self.rooms[self.room]
            else:
                # general member exit from the room
                self.rooms[self.room]["members"].remove(self.phone)

        self.logger.info("websocket closed.")

    def on_message(self, message):
        if message == "monitor_begin":
            self.rooms[self.room]["status"] = room_pool.RUNNING
            return
        if message == "monitor_finish":
            self.rooms[self.room]["status"] = room_pool.ENDING
            return

        # admin recieve other's imgs
        if self.phone == self.rooms[self.room]["admin"]:
            self.write_message(self.rooms[self.room]["real_imgs"])
            return

        is_monitoring = self.rooms[self.room]["status"]

        # img-tag's src start with `data:image/webp;base64,`, but it's not a part of image
        base64_webp_str = re.sub("^data:image/webp;base64,", "", message)

        jpeg = utils.webp_2_others(base64_webp_str)
        # jpeg_face = self.face.mark_face_position(jpeg)
        jpeg_face, result = self.face.mark_68_and_sleepy_points(jpeg)
        default_data = {
            "job_id": self.rooms[self.room]["unique_id"],
            "phone": self.phone,
            "meeting_number_str": str(self.room),
            "sleepy": False,
            "detected_face": False,
            "smile": False,
            "speak": False,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        data = {**default_data, **result}
        self.db_operator.insert_history(data)

        base64_jpeg_str = utils.b64encode_image(jpeg_face)
        img_tag_src = "".join(["data:image/jpeg;base64,", base64_jpeg_str])

        self.rooms[self.room]["real_imgs"][self.phone] = img_tag_src
        self.write_message({self.phone: img_tag_src})


API_NAME = "/real_time"
APIClassObj = RealTimeAPI
