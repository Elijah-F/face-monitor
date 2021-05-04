from collections import defaultdict

import common


@common.hungry_singleton
class RoomPool:
    def __init__(self):
        self.pool = defaultdict(list)

    def __iter__(self):
        return iter(self.pool)

    def __getitem__(self, key):
        return self.pool[key]
