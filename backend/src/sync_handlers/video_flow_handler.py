#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict

import cv2
import tornado.web
from helpers import face_helper, utils

# The higher the value, the lower the accuracy
Precision = 20


class VideoFlowAPI(tornado.web.RequestHandler):
    face_helper = face_helper.FaceHelper()

    def post(self):
        video = self.request.files["video"][0]

        with open("/".join(["../cache", video["filename"]]), "wb") as img:
            img.write(video["body"])

        cap = cv2.VideoCapture("/".join(["../cache", video["filename"]]))

        frame_number = -1
        proof_image = {"face": list(), "sleepy": list(), "smile": list(), "speak": list()}
        origin_data = {"face": 0, "sleepy": 0, "smile": 0, "speak": 0, "normal": 0}

        while True:
            frame_number += 1
            ret, frame = cap.read()
            if not ret:
                break

            if frame_number % Precision == 0:
                mark_image, result = self.face_helper.mark_68_and_sleepy_points(frame, False)

                if not result["detected_face"]:
                    proof_image["face"].append("".join(["data:image/jpeg;base64,", utils.b64encode_image(mark_image)]))
                    origin_data["face"] += 1

                elif result["sleepy"]:
                    proof_image["sleepy"].append(
                        "".join(["data:image/jpeg;base64,", utils.b64encode_image(mark_image)])
                    )
                    origin_data["sleepy"] += 1

                elif result["smile"]:
                    proof_image["smile"].append("".join(["data:image/jpeg;base64,", utils.b64encode_image(mark_image)]))
                    origin_data["smile"] += 1

                else:
                    origin_data["normal"] += 1

        data = [{"type": key, "value": value} for key, value in origin_data.items()]

        self.write({"image": proof_image, "pie": data})


API_NAME = "/video_flow"
APIClassObj = VideoFlowAPI
