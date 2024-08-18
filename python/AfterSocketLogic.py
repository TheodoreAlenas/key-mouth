
# License at the bottom

from db_exceptions import RoomExistsException, RoomDoesntExistException
from Conn import Conn
from logic_and_conn import ConnRoomData, ConfTiming

class LogicHttpException(Exception):
    def __init__(self, detail, status_code):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class AfterSocketLogic:

    def __init__(self, time, db, conf_timing):
        self._conf_timing = conf_timing
        self.db = db
        self.last_id = -1
        self.conns = {}
        self.rooms_ram = {}
        for d in self.db.get_restart_data():
            self.rooms_ram[d.room_id] = ConnRoomData(
                last_moment_time=d.last_moment_time,
                room_id=d.room_id,
                name=d.name,
                db_room=db.get_room(d.room_id))

    def create_room(self, time, name):
        def create_and_set():
            self.db.create_room(time, name)
            self.rooms_ram[name] = ConnRoomData(
                time, name, self.db.get_room(name))
            return ([], None)
        return self._if_room_doesnt_exist(name, create_and_set)

    def delete_room(self, time, name):
        def delete():
            self.db.delete_room(name)
            self.rooms_ram.pop(name)
            return ([], None)
        return self._if_room_exists(name, delete)

    def rename_room(self, time, room_and_name):
        room_id, name = room_and_name
        def rename():
            self.rooms_ram[room_id].rename(name)
            return ([], None)
        return self._if_room_exists(room_id, rename)

    def _if_room_doesnt_exist(self, name, callback):
        try:
            if name in self.rooms_ram:
                raise RoomExistsException()
            return callback()
        except RoomExistsException:
            raise LogicHttpException(f"room '{name}' exists",
                                     status_code=409)

    def _if_room_exists(self, name, callback):
        try:
            if not name in self.rooms_ram:
                raise RoomDoesntExistException()
            return callback()
        except RoomDoesntExistException:
            raise LogicHttpException(f"room '{name}' doesn't exist",
                                     status_code=404)

    def get_rooms(self, _time, _arg):
        ans = []
        for r in self.rooms_ram:
            ans.append({"id": r, "name": self.rooms_ram[r].name})
        return ([], ans)

    def get_moments_range(self, _, room_start_end):
        room, start, end = room_start_end
        def f():
            r = self.rooms_ram[room]
            if start is None and end is None:
                return ([], r.moments.get_last_few())
            return ([], r.moments.get_range(start, end))
        return self._if_room_exists(room, f)

    def connect(self, time, room):
        if not room in self.rooms_ram:
            raise LogicHttpException(f"room '{room}' doesn't exist",
                                     status_code=404)
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Conn(i, self.rooms_ram[room], self._conf_timing)
        return self.conns[i].connect(time, None)


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
