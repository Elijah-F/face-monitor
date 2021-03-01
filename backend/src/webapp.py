#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from common import Config, Logger
from handler_container import HandlerContainer


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")


def start_webapp():
    api_handlers = []
    api_handlers.append((r"/", MainHandler))

    for item in HandlerContainer().api_handlers():
        api_handlers.append(item)

    Logger.info("total api handler: %s", api_handlers)

    app = tornado.web.Application(api_handlers)
    listen_port = int(Config.get("server", "svr_port"))

    app.listen(listen_port)
    tornado.ioloop.IOLoop.current().start()
