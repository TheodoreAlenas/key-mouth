
# License at the bottom

from db_exceptions import RoomExistsException, RoomDoesntExistException
from Conn import Conn
from logic_and_conn import ConnRoomData, ConfTiming

class LogicHttpException(Exception):
    def __init__(self, detail, status_code):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


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
            if not room in self.rooms_ram:
                raise RoomDoesntExistException()
            r = self.rooms_ram[room]
            if start is None and end is None:
                return ([], r.moments.get_last_few())
            return ([], r.moments.get_range(start, end))
        except RoomDoesntExistException:
            raise LogicHttpException("room " + room + " doesn't exist",
                                     status_code=404)

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
