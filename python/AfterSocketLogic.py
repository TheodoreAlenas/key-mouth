
class Moments:
    pass


class Conn:

    def __init__(self, time):
        self.last_spoke = time


class AfterSocketLogic:

    last_id = -1
    last_moment = -1
    conns = {}
    recent_ungrouped = []

    def __init__(self, _, moments_db, min_silence):
        self.min_silence = min_silence
        self.moments = moments_db

    def cleanup(self):
        self.conns.clear()
        self.recent_ungrouped.clear()

    def register(self, time):
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Conn(time)
        return ([], i)

    def disconnect(self, _, conn_id):
        self.conns.pop(conn_id)
        return []

    def handle_input(self, time, conn_id, data):
        if data == "+":
            return []
        self.recent_ungrouped.append({
            "connId": conn_id,
            "type": "write",
            "body": data
        })
        s = self.update(time)
        self.conns[conn_id].last_spoke = time
        return s

    def update(self, time):
        for conn in self.conns:
            if time - self.conns[conn].last_spoke > self.min_silence:
                self.last_moment += 1
        s = {"lastMoment": self.last_moment,
             "curMoment": self.recent_ungrouped}
        return [(conn, s) for conn in self.conns]
