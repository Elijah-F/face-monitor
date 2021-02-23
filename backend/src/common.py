#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
from configparser import ConfigParser

from .helpers.db_helper import DatabaseHelper


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


_path = os.path.dirname(__file__)
Config = init_config(_path + "/../../etc/config.ini")
Db_helper = init_db()
