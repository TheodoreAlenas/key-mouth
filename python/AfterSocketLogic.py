
# License at the bottom

from Connection import Connection, Broadcaster
from exceptions import LogicHttpException
from db.event_adapter import db_model_to_events
from OutputMapper import OutputMapper
from dataclasses import dataclass
from Rooms import Rooms


class AfterSocketLogic:

    def __init__(self, time, db, conf_timing, moments_per_page):
        self._conf_timing = conf_timing
        self.db = db
        saved = self.db.reload_state()
        if saved is None:
            self.last_id = 100
        else:
            self.last_id = saved.last_id
        self.conns = {}
        restart_data = db.get_restart_data()
        self.rooms = Rooms(
            time=time,
            db=db,
            rooms_restart_data=restart_data,
            moments_per_page=moments_per_page,
        )
        for room in self.rooms.get_all():
            room.conn_bcaster = Broadcaster(0, room, self._conf_timing)
            room.conn_bcaster.say_started(time)

    def if_room_is_missing_throw(self, room_id):
        def f(_):
            pass
        self.rooms.given(room_id, f)

    def connect(self, time, room_id):
        def create_conn(room):
            self.last_id += 1
            i = self.last_id
            self.conns[i] = Connection(i, room, self._conf_timing)
            return self.conns[i].connect(time, None)
        return self.rooms.given(room_id, create_conn)

    def create_room(self, time, room_id):
        self.rooms.create(time, room_id)
        def create_bcaster(room):
            room.conn_bcaster = Broadcaster(0, room, self._conf_timing)
            room.conn_bcaster.say_created(time)
            return ([], None)
        return self.rooms.given(room_id, create_bcaster)

    def delete_room(self, time, room_id):
        self.rooms.delete(room_id)
        return ([], None)

    def rename_room(self, _, room_and_name):
        self.rooms.rename(room_and_name[0], room_and_name[1])
        return ([], None)

    def get_rooms(self, _time, _arg):
        return ([], [{"id": r.room_id, "name": r.name}
                     for r in self.rooms.get_all()])

    def get_moments_range(self, _, room_start_end):
        room_id, start, end = room_start_end
        def f(r):
            db_model = r.db.get_range(start, end)
            first = start
            events = db_model_to_events(db_model)
            to_stream = OutputMapper(first, 0)
            for e in events:
                to_stream.push(e)
            return ([], to_stream.stream_models)
        return self.rooms.given(room_id, f)

    def close(self, time, _):
        for room in self.rooms.get_all():
            room.conn_bcaster.close_room(time)
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
