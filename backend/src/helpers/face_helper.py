#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Tuple

import common
import cv2
import dlib
import numpy as np
from imutils import face_utils
from scipy.spatial import distance

K = [
    6.5308391993466671e002,
    0.0,
    3.1950000000000000e002,
    0.0,
    6.5308391993466671e002,
    2.3950000000000000e002,
    0.0,
    0.0,
    1.0,
]
D = [7.0834633684407095e-002, 6.9140193737175351e-002, 0.0, 0.0, -1.3073460323689292e000]

cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)

object_pts = np.float32(
    [
        [6.825897, 6.760612, 4.402142],
        [1.330353, 7.122144, 6.903745],
        [-1.330353, 7.122144, 6.903745],
        [-6.825897, 6.760612, 4.402142],
        [5.311432, 5.485328, 3.987654],
        [1.789930, 5.393625, 4.413414],
        [-1.789930, 5.393625, 4.413414],
        [-5.311432, 5.485328, 3.987654],
        [2.005628, 1.409845, 6.165652],
        [-2.005628, 1.409845, 6.165652],
        [2.774015, -2.080775, 5.048531],
        [-2.774015, -2.080775, 5.048531],
        [0.000000, -3.116408, 6.097667],
        [0.000000, -7.415691, 4.070434],
    ]
)

reprojectsrc = np.float32(
    [
        [10.0, 10.0, 10.0],
        [10.0, 10.0, -10.0],
        [10.0, -10.0, -10.0],
        [10.0, -10.0, 10.0],
        [-10.0, 10.0, 10.0],
        [-10.0, 10.0, -10.0],
        [-10.0, -10.0, -10.0],
        [-10.0, -10.0, 10.0],
    ]
)

line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]


class FaceHelper:
    face_landmark_path = "../tools/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)

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
        face_position = face_detector.detectMultiScale(gray_image, scaleFactor=1.03, minNeighbors=3, minSize=(40, 40))

        # draw square for face
        for x, y, w, h in face_position:
            cv2.rectangle(image, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

        # free RAM, as called by C++
        cv2.destroyAllWindows()

        # save image in buffer
        is_successed, buf = cv2.imencode(".jpeg", image)
        return buf.tobytes()

    def mark_68_and_sleepy_points(self, jpeg_image: bytes) -> Tuple[bytes, dict]:
        # read image
        nparr = np.fromstring(jpeg_image, dtype=np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray_image = cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY)
        result = {"x": 0, "y": 0, "z": 0, "detected_face": False, "sleepy": False, "smile": False}

        # smile detection
        smile_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, "haarcascade_smile.xml"))
        smiles = smile_cascade.detectMultiScale(gray_image, scaleFactor=1.5, minNeighbors=15)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(image, (sx, sy), ((sx + sw), (sy + sh)), (0, 255, 0), 1)
            result["smile"] = True

        face_rects = self.detector(gray_image, 0)

        if len(face_rects) > 0:
            result["detected_face"] = True

            origin_shape = self.predictor(gray_image, face_rects[0])
            shape = face_utils.shape_to_np(origin_shape)

            reprojectdst, euler_angle = self.get_head_pose(shape)
            result["x"] = round(euler_angle[0, 0], 2)
            result["y"] = round(euler_angle[1, 0], 2)
            result["z"] = round(euler_angle[2, 0], 2)

            for start, end in line_pairs:
                cv2.line(image, reprojectdst[start], reprojectdst[end], (0, 0, 255))

            for (x, y) in shape:
                cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

            cv2.putText(
                image,
                "X: " + "{:.2f}".format(euler_angle[0, 0]),
                (20, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                thickness=2,
            )
            cv2.putText(
                image,
                "Y: " + "{:.2f}".format(euler_angle[1, 0]),
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                thickness=2,
            )
            cv2.putText(
                image,
                "Z: " + "{:.2f}".format(euler_angle[2, 0]),
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                thickness=2,
            )

            left_eye, right_eye = list(), list()
            for n in range(36, 42):
                x = origin_shape.part(n).x
                y = origin_shape.part(n).y
                left_eye.append((x, y))
                next_point = n + 1
                if n == 41:
                    next_point = 36
                x2 = origin_shape.part(next_point).x
                y2 = origin_shape.part(next_point).y
                cv2.line(image, (x, y), (x2, y2), (0, 255, 0), 1)

            for n in range(42, 48):
                x = origin_shape.part(n).x
                y = origin_shape.part(n).y
                right_eye.append((x, y))
                next_point = n + 1
                if n == 47:
                    next_point = 42
                x2 = origin_shape.part(next_point).x
                y2 = origin_shape.part(next_point).y
                cv2.line(image, (x, y), (x2, y2), (0, 255, 0), 1)

            left_ear = self.calculate_ear(left_eye)
            right_ear = self.calculate_ear(right_eye)

            ear = round((left_ear + right_ear) / 2, 2)
            if ear < 0.16:
                result["sleepy"] = True
                cv2.putText(image, "Sleepy!", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        is_successed, buf = cv2.imencode(".jpeg", image)
        return buf.tobytes(), result

    def get_head_pose(self, shape):

        image_pts = np.float32(
            [
                shape[17],
                shape[21],
                shape[22],
                shape[26],
                shape[36],
                shape[39],
                shape[42],
                shape[45],
                shape[31],
                shape[35],
                shape[48],
                shape[54],
                shape[57],
                shape[8],
            ]
        )

        _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)
        reprojectdst, _ = cv2.projectPoints(reprojectsrc, rotation_vec, translation_vec, cam_matrix, dist_coeffs)
        reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))

        rotation_mat, _ = cv2.Rodrigues(rotation_vec)
        pose_mat = cv2.hconcat((rotation_mat, translation_vec))
        _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

        return reprojectdst, euler_angle

    def calculate_ear(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear_aspect_ratio = (A + B) / (2.0 * C)
        return ear_aspect_ratio
