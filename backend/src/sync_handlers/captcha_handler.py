import random

import tornado.web


class CaptchaAPI(tornado.web.RequestHandler):
    def post(self):
        captcha = str(random.randint(10000, 99999))
        phone = self.get_body_argument("phone")
        # TODO: tencent cloud sms service


API_NAME = "/captcha"
APIClassObj = CaptchaAPI
