

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
        self.rooms[name] = [[]]

    def add_moment(self, _, room, moment):
        self.rooms[room].append(moment)

    def get_last_few(self, room):
        return self.rooms[room]

    def get_len(self, room):
        return len(self.rooms[room])

    def get_range(self, room, start, end):
        return self.rooms[room][start:end]


class Room:

    def __init__(self, time, name):
        self.name = name
        self.last_moments = []
        self.conns = []
        self.last_moment_notify = None
        self.last_moment_time = time


class Conn:

    def __init__(self, _, conn_id, room, logic):
        self.conn_id = conn_id
        self.room = room
        self._logic = logic
        self.last_spoke = 0.0

    def disconnect(self, time, _):
        s = self._logic.disconnect(time, self.conn_id)
        self.conn_id = None
        self.room = None
        self.logic = None
        return s

    def handle_input(self, time, data):
        return self._logic.handle_input(time, (self, data))

    def update(self, time, _):
        return self._logic.update(time, self.conn_id)


class AfterSocketPublicLogic:

    def __init__(self, logic):
        self._logic = logic
        self.create_room = self._logic.create_room
        self.get_last_few = self._logic.get_last_few
        self.get_moments_range = self._logic.get_moments_range
        self.connect = self._logic.connect


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
        self.rooms[name] = Room(time, name)
        self.moments.add_room(time, name)
        return ([], None)

    def get_last_few(self, _, room):
        return ([], self.moments.get_last_few(room))

    def get_moments_range(self, _, room_start_end):
        room, start, end = room_start_end
        return ([], self.moments.get_range(room, start, end))

    def connect(self, time, room):
        if type(room) != str:
            raise Exception("can't connect with non-string room")
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Conn(time, i, room, self)
        self.rooms[room].conns.append(i)
        s = {"n": None,
             "last": [e for _, e in self.rooms[room].last_moments]}
        return ([(i, s)], self.conns[i])

    def disconnect(self, _, conn_id):
        room = self.rooms[self.conns[conn_id].room]
        room.conns.remove(conn_id)
        self.conns.pop(conn_id)
        return ([], None)

    def handle_input(self, time, conn_and_data):
        conn, data = conn_and_data
        if data == "+":
            return ([], None)
        room = self.rooms[conn.room]
        if room.last_moment_notify is not None:
            room.last_moment_notify = None
        if time - conn.last_spoke > self.min_silence and \
           time - room.last_moment_time > self.min_moment:
            room.last_moment_notify = [e for _, e in room.last_moments]
            self.moments.add_moment(time, conn.room, room.last_moment_notify)
            room.last_moments = []
            room.last_moment_time = time
        conn.last_spoke = time
        room.last_moments.append((time, {
            "connId": conn.conn_id,
            "type": "write",
            "body": data
        }))
        return (self._update(time, room), None)

    def update(self, time, conn_id):
        room = self.rooms[self.conns[conn_id].room]
        return (self._update(time, room), None)

    def _update(self, time, room):
        s = {"n": self.moments.get_len(room.name),
             "last": [e for _, e in room.last_moments]}
        return [(conn, s) for conn in room.conns]

