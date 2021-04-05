import common
import tornado.websocket


class RealTimeAPI(tornado.websocket.WebSocketHandler):
    logger = common.init_logger("real_time")

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
        # TODO: decode the image/webp type file
        #       and tackle it head-on with cv2 or dlib lib
        #       return the handled image for showing in frontend
        self.write_message("okok")


API_NAME = "/real_time"
APIClassObj = RealTimeAPI
