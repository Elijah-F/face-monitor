import re

import common
import tornado.websocket
from helpers import face_helper, utils


class RealTimeAPI(tornado.websocket.WebSocketHandler):
    logger = common.init_logger("real_time")
    face = face_helper.FaceHelper()

    def check_origin(self, origin):
        allowed = ["http://192.168.12.133:8998"]
        if origin not in allowed:
            self.logger.info("not allowed origin %s", origin)
            return False
        return True

    def open(self, *args, **kwargs):
        self.logger.info("new websocket opened.")

    def on_close(self):
        self.logger.info("websocket closed.")

    def on_message(self, message):
        # img-tag's src start with `data:image/webp;base64,`, but it's not a part of image
        base64_webp_str = re.sub("^data:image/webp;base64,", "", message)

        jpeg = utils.webp_2_others(base64_webp_str)
        jpeg_face = self.face.mark_face_position(jpeg)

        base64_jpeg_str = utils.b64encode_image(jpeg_face)
        img_tag_src = "".join(["data:image/jpeg;base64,", base64_jpeg_str])

        self.write_message(img_tag_src)


API_NAME = "/real_time"
APIClassObj = RealTimeAPI
