
# License at the bottom

class LogicHttpException(Exception):
    def __init__(self, detail, status_code):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


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


class Moments:

    def __init__(self, time):
        self.last_time = time
        self.rooms = {}

    def add_room(self, _, name):
        self.rooms[name] = RoomMoments(name, [[]])

    def add_moment(self, time, room, moment):
        self.rooms[room].add_moment(moment, time)

    def get_last_few(self, room):
        return self.rooms[room].get_last_few()

    def get_len(self, room):
        return self.rooms[room].get_len()

    def get_range(self, room, start, end):
        return self.rooms[room].get_range(start, end)


class Room:

    def __init__(self, time, name):
        self.name = name
        self.last_moment = []
        self.conns = []
        self.last_moment_time = time


class Conn:

    def __init__(self, conn_id, room: Room, logic, room_moments: RoomMoments):
        self.conn_id = conn_id
        self.room = room
        self._logic = logic
        self._moments = room_moments
        self.last_spoke = 0.0

    def disconnect(self, time, _):
        s = self._logic.disconnect(time, self.conn_id)
        self.conn_id = None
        self.room = None
        self.logic = None
        return s

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
        started_speaking = (time - self.last_spoke > self._logic.min_silence)
        moment_lasted = (time - self.room.last_moment_time > self._logic.min_moment)
        return started_speaking and moment_lasted

    def _bake_moment_to_be_stored(self, time):
        baked_moment = [e for _, e in self.room.last_moment]
        self._moments.add_moment(time, baked_moment)
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
        s = {"n": self._moments.get_len(),
             "last": [e for _, e in self.room.last_moment]}
        return ([(conn, s) for conn in self.room.conns], None)


class AfterSocketPublicLogic:

    def __init__(self, logic):
        self._logic = logic
        self.create_room = self._logic.create_room
        self.get_rooms = self._logic.get_rooms
        self.get_moments_range = self._logic.get_moments_range
        self.connect = self._logic.connect


class AfterSocketLogic:

    def __init__(self, time, moments_db, min_silence, min_moment):
        self.min_silence = min_silence
        self.min_moment = min_moment
        self.moments = moments_db
        self.last_id = -1
        self.conns = {}
        self.rooms = {}

    def create_room(self, time, name):
        if name in self.rooms:
            raise LogicHttpException("room " + name + " exists",
                                     status_code=409)
        self.rooms[name] = Room(time, name)
        self.moments.add_room(time, name)
        return ([], None)

    def get_rooms(self, _time, _arg):
        return ([], [r for r in self.rooms])

    def get_moments_range(self, _, room_start_end):
        room, start, end = room_start_end
        try:
            if start is None and end is None:
                return ([], self.moments.get_last_few(room))
            return ([], self.moments.get_range(room, start, end))
        except Exception as e:
            raise Exception("(room, start, end) = (" +
                            room + ', ' +
                            str(start) + ', ' +
                            str(end) + ')')

    def connect(self, _, room):
        if type(room) != str:
            raise Exception("can't connect with non-string room")
        if not room in self.rooms:
            raise LogicHttpException("room " + str(room) +
                                     "doesn't exist", status_code=404)
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Conn(i, self.rooms[room], self, self.moments.rooms[room])
        self.rooms[room].conns.append(i)
        s = {"n": self.moments.get_len(room),
             "last": [e for _, e in self.rooms[room].last_moment]}
        return ([(i, s)], self.conns[i])

    def disconnect(self, _, conn_id):
        room = self.rooms[self.conns[conn_id].room.name]
        room.conns.remove(conn_id)
        self.conns.pop(conn_id)
        return ([], None)


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
