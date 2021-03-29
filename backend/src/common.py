#!/usr/bin/env python3
# -*- coding: utf8 -*-

import logging
import logging.handlers
import os
from configparser import ConfigParser

from helpers.db_helper import DatabaseHelper


def init_config(conf_path):
    if not os.path.exists(conf_path):
        raise Exception(f"{conf_path} not found!")

    config = ConfigParser()
    config.read(conf_path)

    return config


def init_db():
    db_conf = dict()
    db_conf["db"] = Config.get("db", "db")
    db_conf["host"] = Config.get("db", "host")
    db_conf["port"] = Config.getint("db", "port")
    db_conf["user"] = Config.get("db", "user")
    db_conf["passwd"] = Config.get("db", "passwd")
    return DatabaseHelper(**db_conf)


def init_logger(name, log_path=None):
    log_file = ""
    if log_path is None:
        log_path = Config.get("server", "log_path")
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        file_name = "".join([name, ".log"])
        log_file = os.path.join(_path, log_path, file_name)

    logger = logging.getLogger(name)

    if name not in _LOGGERS:
        _LOGGERS.append(name)

        handler = logging.handlers.RotatingFileHandler(log_file, "a", maxBytes=104857600, backupCount=10)

        log_format = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s:" "%(lineno)d] %(message)s"
        )
        handler.setFormatter(log_format)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger


def hungry_singleton(cls):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


def get_job_name(path):
    """ transform 'xxx/xxx/xxx/abc_def_handler.py' into 'abc_def' """
    return os.path.basename(path)[:-11]


def change_dir():
    """ change work dir from 'face_monitor' to 'face_monitor/backend/src' """
    old_dir = os.getcwd()
    new_dir = "/".join([old_dir, "backend/src"])
    os.chdir(new_dir)


_LOGGERS = list()
_path = os.path.dirname(__file__)
Config = init_config(_path + "/../etc/config.ini")
Db_helper = init_db()
Logger = init_logger("server")
