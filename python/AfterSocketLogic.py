
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
        return None

    def update(self, time):
        return None


class AfterSocketLogic:

    last_id = -1
    divider = DiffDivider()

    def __init__(self, moments_db):
        self.moments = moments_db

    def register(self, socket_object):
        self.last_id += 1
        i = self.last_id
        return i

    def handle_input(self, conn_id, data, time):
        res = self.divider.new_diff(time, conn_id)
        if res is not None:
            print("new moment packaged")
        return [(conn_id,
                 [{"connId": 4, "type": "write", "body": "hello"}])]
