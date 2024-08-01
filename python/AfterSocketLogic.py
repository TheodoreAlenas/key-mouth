
class ConnectionState:

    inputFieldText = ""

    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.name = "connection#" + str(conn_id)


class Moments:

    m = []

    def push(self, moment):
        self.m.append(moment)

    def get(self, i):
        return self.m[i]

    def size(self):
        return len(self.m)


def get_diff(a, b):
    if str.startswith(b, a):
        return {
            "action": "wrote",
            "body": b[len(a):],
        }
    if str.startswith(a, b):
        return {
            "action": "deleted",
            "n": len(a) - len(b) + 1,
        }
    return {
        "action": "changed",
        "prev": a,
        "next": b,
    }


class DiffDivider:

    def new_diff(self, time, conn_id):
        return 1

    def update(self, time):
        return None


def diff_accumulate(state, diffs):
    return []


class AfterSocketLogic:

    last_id = -1
    moments = Moments()
    conns = {}

    def register(self, socket_object):
        self.last_id += 1
        i = self.last_id
        self.conns[i] = ConnectionState(i)
        return i

    def get_json(self, data, time):
        return {
            "states": [],
            "diffs": [{"connId": 4, "type": "write", "body": "hello"}]
        }

    def get_last_n_moments(self, n):
        pass
