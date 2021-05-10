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
        bar, pie, line, job_date = defaultdict(list), defaultdict(list), list(), dict()

        for row in rows:
            data[row["job_id"]]["face"] += row["detected_face"]
            data[row["job_id"]]["sleepy"] += row["sleepy"]
            data[row["job_id"]]["speak"] += row["speak"]
            data[row["job_id"]]["smile"] += row["smile"]
            data[row["job_id"]]["total_abnormal"] += (
                not row["detected_face"] or row["sleepy"] or row["speak"] or row["smile"]
            )
            data[row["job_id"]]["total"] += 1

            if row["job_id"] not in job_date:
                job_date[row["job_id"]] = str(row["insert_time"])

        for key, value in data.items():
            indexs = ["face", "sleepy", "speak", "smile"]

            for index in indexs:
                if index == "face":
                    bar[key].append({"index": index, "proportion": "abnormal", "value": value["total"] - value[index]})
                    bar[key].append({"index": index, "proportion": "general", "value": value[index]})
                    continue

                bar[key].append({"index": index, "proportion": "abnormal", "value": value[index]})
                bar[key].append({"index": index, "proportion": "general", "value": value["total"] - value[index]})

            pie[key].append({"type": "异常情况", "value": value["total_abnormal"]})
            pie[key].append({"type": "正常情况", "value": value["total"] - value["total_abnormal"]})

        for job_id, date in job_date.items():
            indexs = ["face", "sleepy", "speak", "smile"]

            for index in indexs:
                if index == "face":
                    line.append(
                        {
                            "time": date,
                            "index": index,
                            "value": round((data[job_id]["total"] - data[job_id][index]) / data[job_id]["total"], 2),
                        }
                    )
                    continue
                line.append(
                    {
                        "time": date,
                        "index": index,
                        "value": round(data[job_id][index] / data[job_id]["total"], 2),
                    }
                )

        self.write({"bar": bar, "pie": pie, "line": line, "job_date": job_date})


API_NAME = "/history"
APIClassObj = HistoryAPI
