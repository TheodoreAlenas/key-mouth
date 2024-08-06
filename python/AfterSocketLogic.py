
class Moments:

    def __init__(self, time):
        self.last_time = time

    def get_last_few(self):
        return [
            [
                {"connId": 4, "type": "write", "body": "H"},
                {"connId": 4, "type": "write", "body": "i"},
                {"connId": 4, "type": "write", "body": " Mst"},
                {"connId": 4, "type": "delete", "body": "s"},
                {"connId": 4, "type": "delete", "body": "t"},
                {"connId": 4, "type": "write", "body": "ark"}
            ],
            [
                {"connId": 4, "type": "write", "body": "r u there?"},
                {"connId": 5, "type": "write",
                 "body": "I thought I'd find you here"}
            ]
        ]


class Conn:

    def __init__(self, _, room):
        self.room = room


class Room:

    def __init__(self, _):
        self.last_moments = []
        self.conns = []


class AfterSocketLogic:

    def __init__(self, time, moments_db, min_silence, min_moment):
        self.min_silence = min_silence
        self.min_moment = min_moment
        self.moments = moments_db
        self.last_id = -1
        self.last_moment = -1
        self.conns = {}
        self.rooms = {}

    def create_room(self, time, name):
        self.rooms[name] = Room(time)

    def get_last_few(self, room):  # NO TEST COVERAGE
        last = [e for _, e in self.rooms[room].last_moments]
        return self.moments.get_last_few() + [last]

    def register(self, time, session):
        if type(session) != str:
            raise Exception("can't register with non-string room")
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Conn(time, session)
        self.rooms[session].conns.append(i)
        return ([], i)

    def disconnect(self, _, conn_id):
        self.rooms[self.conns[conn_id].room].conns.pop(conn_id)
        self.conns.pop(conn_id)
        return ([], None)

    def handle_input(self, time, conn_id_and_data):
        conn_id, data = conn_id_and_data
        if data == "+":
            return ([], None)
        self.rooms[self.conns[conn_id].room].last_moments.append((time, {
            "connId": conn_id,
            "type": "write",
            "body": data
        }))
        s = self.update(time, conn_id)
        return s

    def update(self, time, conn_id):
        s = {"lastMoment": None,
             "curMoment": [e for _, e in self.rooms[self.conns[conn_id].room].last_moments]}
        return ([(conn, s) for conn in self.rooms[self.conns[conn_id].room].conns], None)
