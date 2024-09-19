
# License at the bottom

from db.exceptions import RoomExistsException, RoomDoesntExistException
from exceptions import LogicHttpException
from Room import Room
from MomentSplitter import ConfTiming, MomentSplitterData


class Rooms:

    def __init__(self, time, db, rooms_restart_data, moments_per_page):
        self.db = db
        self.rooms_ram = {}
        self.moments_per_page = moments_per_page
        for d in rooms_restart_data:
            r = Room(
                splitter_data=MomentSplitterData(
                    last_moment_time=None,
                ),
                room_id=d.room_id,
                name=d.name,
                db_room=db.get_room(d.room_id),
                moments_per_page=self.moments_per_page,
            )
            # TODO: call the page splitter using the incomplete page
            self.rooms_ram[d.room_id] = r

    def create(self, time, room_id):
        def create_and_set():
            self.db.create_room(time, room_id)
            r = Room(
                splitter_data=MomentSplitterData(
                    last_moment_time=time,
                ),
                room_id=room_id,
                db_room=self.db.get_room(room_id),
                moments_per_page=self.moments_per_page,
            )
            self.rooms_ram[room_id] = r
        self.without(room_id, create_and_set)

    def delete(self, room_id):
        def delete(_):
            self.db.delete_room(room_id)
            self.rooms_ram.pop(room_id)
        self.given(room_id, delete)

    def rename(self, room_id, name):
        def rename_it(room):
            room.rename(name)
        self.given(room_id, rename_it)

    def get_all(self):
        return [self.rooms_ram[r] for r in self.rooms_ram]

    def given(self, room_id, callback):
        try:
            if not room_id in self.rooms_ram:
                raise RoomDoesntExistException()
            return callback(self.rooms_ram[room_id])
        except RoomDoesntExistException:
            raise LogicHttpException(f"room '{room_id}' doesn't exist",
                                     status_code=404)

    def without(self, room_id, callback):
        try:
            if room_id in self.rooms_ram:
                raise RoomExistsException()
            return callback()
        except RoomExistsException:
            raise LogicHttpException(f"room '{room_id}' exists",
                                     status_code=409)


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
