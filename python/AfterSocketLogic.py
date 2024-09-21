
# License at the bottom

from MomentSplitter import MomentSplitter
from Connection import Connection, Broadcaster
from exceptions import LogicHttpException
from db.event_adapter import db_model_to_events
from OutputMapper import OutputMapper
from dataclasses import dataclass
from Rooms import Rooms
from RoomReloader import RoomReloader


class RoomReloaderLimitedDb:

    def __init__(self, db):
        self.db = db
        self.get_reloadable_state = db.get_reloadable_state
        self.set_reloadable_state = db.set_reloadable_state
        self.get_restart_data = db.get_restart_data
        self.get_room = db.get_room


class AfterSocketLogic:

    def __init__(self, time, db, conf_timing, moments_per_page):
        self._conf_timing = conf_timing
        self.db = db
        self.room_reloader = RoomReloader(
            moments_per_page=moments_per_page,
            db=RoomReloaderLimitedDb(db),
        )
        self.conns = {}
        self.rooms = Rooms(
            db=db,
            room_reloader=self.room_reloader,
        )
        saved = self.rooms.load()
        self.last_id = 100
        if saved is not None:
            self.last_id = saved.last_id
        for room in self.rooms.get_all():
            room.conn_bcaster = Broadcaster(
                conn_id=0,
                room=room,
                moment_splitter=MomentSplitter(
                    conf_timing=self._conf_timing,
                    room=room.moment_splitter_data,
                )
            )
            room.conn_bcaster.say_started(time)

    def if_room_is_missing_throw(self, room_id):
        def f(_):
            pass
        self.rooms.given(room_id, f)

    def connect(self, time, room_id):
        def create_conn(room):
            self.last_id += 1
            i = self.last_id
            self.conns[i] = Connection(
                conn_id=i,
                room=room,
                moment_splitter=MomentSplitter(
                    conf_timing=self._conf_timing,
                    room=room.moment_splitter_data,
                )
            )
            return self.conns[i].connect(time, None)
        return self.rooms.given(room_id, create_conn)

    def create_room(self, time, room_id):
        self.rooms.create(time, room_id)
        def create_bcaster(room):
            room.conn_bcaster = Broadcaster(
                conn_id=0,
                room=room,
                moment_splitter=MomentSplitter(
                    conf_timing=self._conf_timing,
                    room=room.moment_splitter_data,
                )
            )
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

    def get_pages_range(self, _, room_start_end):
        room_id, start, end = room_start_end
        def f(r):
            db_model = r.db.get_range(start, end)
            first = start
            events = db_model_to_events(db_model)
            to_stream = OutputMapper(first, 0)
            for e in events:
                to_stream.push(e)
            return ([], to_stream.get_last_page())
        return self.rooms.given(room_id, f)

    def close(self, time, _):
        self.room_reloader.close(
            time=time,
            last_id=self.last_id,
            rooms=self.rooms.get_all(),
        )
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
