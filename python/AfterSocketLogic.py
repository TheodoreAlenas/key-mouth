
class Moments:

    m = []

    def __init__(self, time):
        self.last_time = time

    def append(self, time, moment):
        self.m.append((time, moment))
        self.last_time = time

    def get_len(self):
        return len(self.m)

    def get_last_time(self):
        return self.last_time


class Conn:

    def __init__(self, time):
        self.last_spoke = time


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
        self._maybe_inc_last_moment(time)
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
        self.conns[conn_id].last_spoke = time
        return s

    def update(self, time, _):
        for conn in self.conns:
            l = self.conns[conn].last_spoke
            if time - l > self.min_silence:
                self._maybe_inc_last_moment(l)
        s = {"lastMoment": self.moments.get_len() - 1,
             "curMoment": [e for _, e in self.recent_ungrouped]}
        return ([(conn, s) for conn in self.conns], None)

    def _maybe_inc_last_moment(self, time):
        if time - self.moments.get_last_time() < self.min_moment:
            return
        l = 0
        for t, m in self.recent_ungrouped:
            if t > time:
                break
            l += 1
        self.moments.append(time, self.recent_ungrouped[:l])
        self.recent_ungrouped = self.recent_ungrouped[l:]
