
class Moments:

    def __init__(self, time):
        self.last_time = time


class Conn:

    def __init__(self, time):
        pass


class AfterSocketLogic:

    last_id = -1
    last_moment = -1
    conns = {}
    recent_ungrouped = []

    def __init__(self, time, moments_db, min_silence, min_moment):
        self.min_silence = min_silence
        self.min_moment = min_moment
        self.moments = moments_db

    def cleanup(self):
        self.conns.clear()
        self.recent_ungrouped.clear()

    def register(self, time, _):
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Conn(time)
        return ([], i)

    def disconnect(self, _, conn_id):
        self.conns.pop(conn_id)
        return ([], None)

    def handle_input(self, time, conn_id_and_data):
        conn_id, data = conn_id_and_data
        if data == "+":
            return ([], None)
        self.recent_ungrouped.append((time, {
            "connId": conn_id,
            "type": "write",
            "body": data
        }))
        s = self.update(time, None)
        return s

    def update(self, time, _):
        s = {"lastMoment": None,
             "curMoment": [e for _, e in self.recent_ungrouped]}
        return ([(conn, s) for conn in self.conns], None)
