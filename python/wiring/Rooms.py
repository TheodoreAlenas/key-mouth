
# License at the bottom

from db.exceptions import RoomExistsException, RoomDoesntExistException
from lib.exceptions import LogicHttpException


class Rooms:

    def __init__(self, db, room_reloader):
        self.db = db
        self.room_reloader = room_reloader

    def load(self):
        self.rooms_ram, saved = self.room_reloader.load()
        return saved

    def create(self, time, room_id):
        def create_and_set():
            self.db.create_room(time, room_id)
            r = self.room_reloader.create(room_id)
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
