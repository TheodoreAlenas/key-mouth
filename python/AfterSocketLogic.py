
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

    def __init__(self, moments_db):
        self.moments = moments_db

    def cleanup(self):
        self.conns.clear()

    def register(self, time):
        self.last_id += 1
        i = self.last_id
        self.conns.append(i)
        return ([], i)

    def disconnect(self, conn_id, time):
        self.conns.remove(conn_id)
        return []

    def handle_input(self, conn_id, data, time):
        if data == "+":
            return []
        res = self.divider.new_diff(time, conn_id)
        if res is not None:
            print("new moment packaged")
        return [(conn,
                 [{"connId": conn_id, "type": "write", "body": "hello"}])
                for conn in self.conns]
