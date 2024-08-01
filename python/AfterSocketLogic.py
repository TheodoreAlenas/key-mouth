
class Moments:

    m = []

    def push(self, moment):
        self.m.append(moment)

    def get(self, i):
        return self.m[i]

    def size(self):
        return len(self.m)


class DiffDivider:

    def new_diff(self, time, conn_id):
        return 1

    def update(self, time):
        return None


class AfterSocketLogic:

    last_id = -1

    def __init__(self, moments_db):
        self.moments = moments_db

    def register(self, socket_object):
        self.last_id += 1
        i = self.last_id
        return i

    def get_json(self, data, time):
        return [{"connId": 4, "type": "write", "body": "hello"}]

    def get_last_n_moments(self, n):
        pass
