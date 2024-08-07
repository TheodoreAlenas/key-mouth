

class LogicHttpException(Exception):
    def __init__(self, detail, status_code):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class Moments:

    def __init__(self, time):
        self.last_time = time
        self.rooms = {"hello": [
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
        ]}

    def add_room(self, _, name):
        self.rooms[name] = []

    def get_last_few(self, room):
        return self.rooms[room]


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
        if name in self.rooms:
            raise LogicHttpException("room " + name + " exists",
                                     status_code=409)
        self.rooms[name] = Room(time)
        self.moments.add_room(time, name)
        return ([], None)

    def get_last_few(self, _, room):
        last = [e for _, e in self.rooms[room].last_moments]
        return ([], self.moments.get_last_few(room) + [last])

    def connect(self, time, room):
        if type(room) != str:
            raise Exception("can't connect with non-string room")
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Conn(time, room)
        self.rooms[room].conns.append(i)
        return ([], i)

    def disconnect(self, _, conn_id):
        room = self.rooms[self.conns[conn_id].room]
        room.conns.remove(conn_id)
        self.conns.pop(conn_id)
        return ([], None)

    def handle_input(self, time, conn_id_and_data):
        conn_id, data = conn_id_and_data
        if data == "+":
            return ([], None)
        room = self.rooms[self.conns[conn_id].room]
        room.last_moments.append((time, {
            "connId": conn_id,
            "type": "write",
            "body": data
        }))
        return (self._update(time, room), None)

    def update(self, time, conn_id):
        room = self.rooms[self.conns[conn_id].room]
        return (self._update(time, room), None)

    def _update(self, time, room):
        s = {"lastMoment": None,
             "curMoment": [e for _, e in room.last_moments]}
        return [(conn, s) for conn in room.conns]

