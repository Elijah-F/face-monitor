#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict

import common


@common.hungry_singleton
class RoomPool:
    def __init__(self):
        self.pool = defaultdict(lambda: {"admin": None, "members": [], "real_imgs": {}})

    def __iter__(self):
        return iter(self.pool)

    def __getitem__(self, key):
        return self.pool[key]

    def __delitem__(self, key):
        del self.pool[key]


if __name__ == "__main__":
    room_pool = {
        12345: {"admin": 17729505029, "members": [17729505029, 17729505030], "real_imgs": {}},
        12346: {"admin": 17729505050, "members": [17729505050, 17729505051], "real_imgs": {}},
    }
