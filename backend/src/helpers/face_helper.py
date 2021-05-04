#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import common
import cv2
import numpy as np


class FaceHelper:
    def __init__(self):
        self.logger = common.init_logger("face_helper")

    def mark_face_position(self, jpeg_image: bytes) -> bytes:
        """mark face in image with square
        Args:
            jpeg_image(bytes): image bytes data
        Returns:
            bytes: image bytes data drawed square in face
        """
        # read image from buffer
        nparr = np.fromstring(jpeg_image, dtype=np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # gray image can reduce workloads for CPU
        gray_image = cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY)
        face_detector = cv2.CascadeClassifier(
            os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        )
        face_position = face_detector.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=3, minSize=(80, 80))

        # draw square for face
        for x, y, w, h in face_position:
            cv2.rectangle(image, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

        # free RAM, as called by C++
        cv2.destroyAllWindows()

        # save image in buffer
        is_successed, buf = cv2.imencode(".jpeg", image)
        return buf.tobytes()
