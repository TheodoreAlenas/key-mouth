
# License at the bottom

from db.exceptions import RoomExistsException, RoomDoesntExistException
from Connection import Connection, Broadcaster
from exceptions import LogicHttpException
from ConnRoomData import ConnRoomData
from MomentSplitter import ConfTiming
from db.event_adapter import db_model_to_events
from EventStreamAdapter import EventStreamAdapter
from dataclasses import dataclass


class AfterSocketLogic:

    def __init__(self, time, db, conf_timing):
        self._conf_timing = conf_timing
        self.db = db
        saved = self.db.reload_state()
        if saved is None:
            self.last_id = 100
        else:
            self.last_id = saved.last_id
        self.conns = {}
        self.rooms_ram = {}
        for d in self.db.get_restart_data():
            self.rooms_ram[d.room_id] = ConnRoomData(
                last_moment_time=d.last_moment_time,
                room_id=d.room_id,
                name=d.name,
                db_room=db.get_room(d.room_id))
            r = self.rooms_ram[d.room_id]
            r.conn_bcaster = Broadcaster(0, r, self._conf_timing)
            r.conn_bcaster.say_started(time)

    def connect(self, time, room):
        if not room in self.rooms_ram:
            raise LogicHttpException(f"room '{room}' doesn't exist",
                                     status_code=404)
        self.last_id += 1
        i = self.last_id
        self.conns[i] = Connection(i, self.rooms_ram[room], self._conf_timing)
        return self.conns[i].connect(time, None)

    def create_room(self, time, room_id):
        def create_and_set():
            self.db.create_room(time, room_id)
            r = ConnRoomData(time, room_id, self.db.get_room(room_id))
            r.conn_bcaster = Broadcaster(0, r, self._conf_timing)
            self.rooms_ram[room_id] = r
            r.conn_bcaster.say_created(time)
            #r.conn_bcaster.handle_input("")
            return ([], None)
        return self._if_room_doesnt_exist(room_id, create_and_set)

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
            db_model = r.db.get_range(start, end)
            first = start
            events = db_model_to_events(db_model)
            to_stream = EventStreamAdapter(first, 0)
            for e in events:
                to_stream.push(e)
            return ([], to_stream.stream_models)
        return self._if_room_exists(room, f)

    def close(self, time, _):
        for room_id in self.rooms_ram:
            self.rooms_ram[room_id].conn_bcaster.close_room(time)
        self.db.save_state(last_id=self.last_id)
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
