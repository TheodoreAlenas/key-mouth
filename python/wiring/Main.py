
# License at the bottom

from lib.exceptions import LogicHttpException
from wiring.Rooms import Rooms
from wiring.RoomReloader import RoomReloader
from wiring.ConnectionFactory import ConnectionFactory


class DbForRoomReloader:

    def __init__(self, db):
        self.get_reloadable_state = db.get_reloadable_state
        self.set_reloadable_state = db.set_reloadable_state
        self.get_restart_data = db.get_restart_data
        self.get_room = db.get_room


class DbForRooms:

    def __init__(self, db):
        self.create_room = db.create_room
        self.delete_room = db.delete_room
        self.get_room = db.get_room


class RoomForConn:

    def __init__(self, room):
        self.room_id = room.room_id
        self.conns = room.conns
        self.page_splitter = room.page_splitter
        self.moment_splitter_data = room.moment_splitter_data
        self.pers_out_map = room.pers_out_map


class Main:

    def __init__(self, time, db,
                 min_silence, min_moment, moments_per_page):
        self.room_reloader = RoomReloader(
            moments_per_page=moments_per_page,
            db=DbForRoomReloader(db),
        )
        self.rooms = Rooms(
            db=DbForRooms(db),
            room_reloader=self.room_reloader,
        )
        saved = self.rooms.load()
        self.new = ConnectionFactory(
            min_silence=min_silence,
            min_moment=min_moment,
            last_id=saved.last_id,
        )
        for room in self.rooms.get_all():
            room.conn_bcaster = self.new.broadcaster(RoomForConn(room))
            room.conn_bcaster.say_started(time)

    def if_room_is_missing_throw(self, room_id):
        def f(_):
            pass
        self.rooms.given(room_id, f)

    def connect(self, time, room_id):
        def create_conn(room):
            conn = self.new.connection(RoomForConn(room))
            return conn.connect(time, None)
        return self.rooms.given(room_id, create_conn)

    def create_room(self, time, room_id):
        self.rooms.create(time, room_id)
        def create_bcaster(room):
            room.conn_bcaster = self.new.broadcaster(RoomForConn(room))
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
        def f(room):
            return ([], room.pers_out_map.get_pages_range(start, end))
        return self.rooms.given(room_id, f)

    def close(self, time, _):
        self.room_reloader.close(
            time=time,
            last_id=self.new.last_id,
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
