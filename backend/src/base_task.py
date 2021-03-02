#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

import common


class BaseTask(ABC):
    def __init__(self, loop, logger):
        self._loop = loop
        self._logger = logger

    async def start(self, data=None):
        result = await self.inner_run(data)
        return result

    @abstractmethod
    async def inner_run(self, job_info):
        return NotImplementedError

    async def exec_shell(self, cmd):
        pass

    async def query_db(self, sql, option="query", data=None):
        """Execute sql statement in thread pool
        https://docs.python.org/3/library/asyncio-eventloop.html#executing-code-in-thread-or-process-pools)

        Args:
            sql    : sql or sql-like statement
            option : db query type, should in {"insert", "update", "query", "execute_many"}. Defaults to "query".
            data   : additional data to pass. Defaults to None.

        Returns:
            db execution result
        """

        result = await self._loop.run_in_executor(None, db_execute, sql, option, data)
        return result


def acquire_oper(option, db_con):
    """determine db handler according to option"""

    if option not in ["query", "update", "insert", "insert_many"]:
        option = "other"

    return {
        "query": db_con.query,
        "update": db_con.update,
        "insert": db_con.insert,
        "insert_many": db_con.insert_many,
        "other": lambda sql, data: None,
    }[option]


def db_execute(sql, option="query", data=None):
    """exec sql according to option, if option is illegal return None"""

    db_con = common.Db_helper
    db_con.connect()

    option_handler = acquire_oper(option, db_con)
    result = option_handler(sql, data)

    db_con.close()
    return result
