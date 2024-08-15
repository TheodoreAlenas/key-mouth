
# License at the bottom

class LogicHttpException(Exception):
    def __init__(self, detail, status_code):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class RoomExistsException(Exception):
    def __init__(self, msg="room already exists"):
        super().__init__(msg)


class RoomDoesntExistException(Exception):
    def __init__(self, msg="room doesn't exist"):
        super().__init__(msg)


class RoomMoments:

    def __init__(self, name, moments):
        self.name = name
        self.moments = moments

    def add_moment(self, _, moment):
        self.moments.append(moment)

    def get_last_few(self):
        m = self.moments
        return {"start": 0, "end": len(m), "moments": m}

    def get_len(self):
        return len(self.moments)

    def get_range(self, start, end):
        return self.moments[start:end]


class DbMock:

    def __init__(self):
        self.rooms = {}

    def create_room(self, _, name):
        if name in self.rooms:
            raise RoomExistsException("[DbMoct] room '" + name +
                                      "' already exists")
        self.rooms[name] = RoomMoments(name, [[]])

    def get_room(self, name) -> RoomMoments:
        if not name in self.rooms:
            raise RoomDoesntExistException("[DbMock] room '" + name +
                                           "' doesn't exist")
        return self.rooms[name]

    def get_rooms_and_their_last_moment_times(self):
        res = []
        for name in self.rooms:
            res.append((name, 0.0))
        return res


class ConnRoomData:

    def __init__(self, time, name, moments):
        self.name = name
        self.last_moment = []
        self.conns = []
        self.last_moment_time = time
        self.moments = moments


class ConfTiming:

    def __init__(self, min_silence, min_moment):
        self.min_silence = min_silence
        self.min_moment = min_moment


class Conn:

    def __init__(self, conn_id, room: ConnRoomData, conf_timing: ConfTiming):
        self.conn_id = conn_id
        self.room = room
        self._conf_timing = conf_timing
        self.last_spoke = 0.0

    def disconnect(self, time, _):
        self.room.conns.remove(self.conn_id)
        return ([], None)

    def handle_input(self, time, data):
        if len(data) < 2:
            return ([], None)
        if data[0] == '+':
            return self._handle_parsed(time, "write", data[1:])
        elif data[0] == '-':
            return self._handle_parsed(time, "delete", data[1:])
        return ([], None)

    def _handle_parsed(self, time, inp_type, body):
        if self._interrupted_conversation(time):
            self._bake_moment_to_be_stored(time)
        self._append_and_update(time, inp_type, body)
        return self._get_last_moment_broadcast_list()

    def _interrupted_conversation(self, time):
        started_speaking = (time - self.last_spoke >
                            self._conf_timing.min_silence)
        moment_lasted = (time - self.room.last_moment_time >
                         self._conf_timing.min_moment)
        return started_speaking and moment_lasted

    def _bake_moment_to_be_stored(self, time):
        baked_moment = [e for _, e in self.room.last_moment]
        self.room.moments.add_moment(time, baked_moment)
        self.room.last_moment = []
        self.room.last_moment_time = time

    def _append_and_update(self, time, inp_type, body):
        self.last_spoke = time
        self.room.last_moment.append((time, {
            "connId": self.conn_id,
            "type": inp_type,
            "body": body
        }))

    def _get_last_moment_broadcast_list(self):
        s = self.get_last_moment_json_list()
        return ([(conn, s) for conn in self.room.conns], None)

    def get_last_moment_json_list(self):
        return {"n": self.room.moments.get_len(),
                "last": [e for _, e in self.room.last_moment]}


class AfterSocketPublicLogic:

    def __init__(self, logic):
        self._logic = logic
        self.create_room = self._logic.create_room
        self.get_rooms = self._logic.get_rooms
        self.get_moments_range = self._logic.get_moments_range
        self.connect = self._logic.connect


class AfterSocketLogic:

    def __init__(self, time, db, conf_timing):
        self._conf_timing = conf_timing
        self.db = db
        self.last_id = -1
        self.conns = {}
        self.rooms_ram = {}
        for n, t in self.db.get_rooms_and_their_last_moment_times():
            self.rooms_ram[n] = ConnRoomData(t, n, db.get_room(n))

    def create_room(self, time, name):
        try:
            self.db.create_room(time, name)
            if name in self.rooms_ram:
                raise RoomExistsException()
            self.rooms_ram[name] = ConnRoomData(
                time, name, self.db.get_room(name))
        except RoomExistsException:
            raise LogicHttpException("room " + name + " exists",
                                     status_code=409)
        return ([], None)

    def get_rooms(self, _time, _arg):
        return ([], [r for r in self.rooms_ram])

    def get_moments_range(self, _, room_start_end):
        room, start, end = room_start_end
        try:
            r = self.rooms_ram[room]
            if start is None and end is None:
                return ([], r.moments.get_last_few())
            return ([], r.moments.get_range(start, end))
        except Exception as e:
            raise Exception("(room, start, end) = (" +
                            room + ', ' +
                            str(start) + ', ' +
                            str(end) + ')')

    def connect(self, _, room):
        if type(room) != str:
            raise Exception("can't connect with non-string room " +
                            str(room))
        if not room in self.rooms_ram:
            raise LogicHttpException("room '" + str(room) +
                                     "' doesn't exist", status_code=404)
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Conn(i, self.rooms_ram[room], self._conf_timing)
        self.rooms_ram[room].conns.append(i)
        s = self.conns[i].get_last_moment_json_list()
        return ([(i, s)], self.conns[i])


"""
Copyright 2024 <dimakopt732@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
