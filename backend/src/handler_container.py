#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from . import common


@common.hungry_singleton
class HandlerContainer:
    def __init__(self):
        self._logger = common.init_logger("handler")
        self._handler_container = list()

        self._handler_name_2_obj = dict()
        self._api_name_2_obj = dict()

    def regist_handler(self, name, obj):
        self._handler_container.append((name, obj))
        self._handler_name_2_obj[name] = obj
        self._logger.info("regist_handler %s", name)

    def regist_api_handler(self, api_name, obj):
        self._api_name_2_obj[api_name] = obj
        self._logger.info("regist_api_handler %s", api_name)

    def get_handler(self, name):
        return self._handler_name_2_obj.get(name, None)

    def get_api_handler(self, name):
        return self._api_name_2_obj.get(name, None)

    def handlers(self):
        for name, obj in self._handler_name_2_obj.items():
            yield (name, obj)

    def api_handlers(self):
        for name, obj in self._api_name_2_obj.items():
            yield (name, obj)


def import_handler(path):
    sys.path.append(path)

    for file_name in os.listdir(path):
        if not file_name.endswith("_handler.py", 0):
            continue

        module_name = file_name[:-3]
        module = __import__(module_name)

        if hasattr(module, "JOB_NAME") and module.JOB_NAME:
            HandlerContainer().regist_handler(module.JOB_NAME, module.ClassOb)

        if hasattr(module, "API_NAME") and module.API_NAME:
            HandlerContainer().regist_api_handler(module.API_NAME, module.APIClassObj)


if __name__ == "__main__":
    pass
