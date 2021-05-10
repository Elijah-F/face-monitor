#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict

import tornado.web
from helpers import db_operator


class HistoryAPI(tornado.web.RequestHandler):
    db_operator = db_operator.DbOperator()

    def get(self):
        phone = self.get_query_argument("phone")

        rows = self.db_operator.select_history(phone)

        data = defaultdict(lambda: defaultdict(int))
        bar, pie = defaultdict(list), defaultdict(list)

        for row in rows:
            data[row["job_id"]]["face"] += row["detected_face"]
            data[row["job_id"]]["sleepy"] += row["sleepy"]
            data[row["job_id"]]["speak"] += row["speak"]
            data[row["job_id"]]["smile"] += row["smile"]
            data[row["job_id"]]["total_abnormal"] += (
                row["detected_face"] or row["sleepy"] or row["speak"] or row["smile"]
            )
            data[row["job_id"]]["total"] += 1

        for key, value in data.items():
            indexs = ["face", "sleepy", "speak", "smile"]
            for index in indexs:
                bar[key].append({"index": index, "proportion": "abnormal", "value": value[index]})
                bar[key].append({"index": index, "proportion": "general", "value": value["total"] - value[index]})
            pie[key].append({"type": "异常情况", "value": value["total_abnormal"]})
            pie[key].append({"type": "正常情况", "value": value["total"] - value["total_abnormal"]})

        self.write({"bar": bar, "pie": pie})


API_NAME = "/history"
APIClassObj = HistoryAPI
