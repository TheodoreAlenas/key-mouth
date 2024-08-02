
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
    conns = []
    recent_ungrouped = []

    def __init__(self, moments_db):
        self.moments = moments_db

    def cleanup(self):
        self.conns.clear()
        self.recent_ungrouped.clear()

    def register(self, _):
        self.last_id += 1
        i = self.last_id
        self.conns.append(i)
        return ([], i)

    def disconnect(self, _, conn_id):
        self.conns.remove(conn_id)
        return []

    def handle_input(self, time, conn_id, data):
        if data == "+":
            return []
        res = self.divider.new_diff(time, conn_id)
        if res is not None:
            print("new moment packaged")
        self.recent_ungrouped.append({
            "connId": conn_id,
            "type": "write",
            "body": data
        })
        return self._to_send()

    def update(self, _):
        return self._to_send()

    def _to_send(self):
        return [(
            conn,
            {"lastMoment": -1, "curMoment": self.recent_ungrouped}
        ) for conn in self.conns]
