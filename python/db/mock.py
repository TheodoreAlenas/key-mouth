
# License at the bottom

from db.exceptions import RoomExistsException, RoomDoesntExistException
from db.mock_and_mongo import *


class DbRoom:

    def __init__(self, room_id):
        self.room_id = room_id
        self.name = None
        self.pages = []

    def rename(self, name):
        self.name = name

    def push_page(self, page):
        self.pages.append(page)

    def get_last_pages(self, n):
        if len(self.pages) < n:
            return LastPages(
                pages=self.pages,
                first_page_idx=0,
            )
        return LastPages(
            pages=self.pages[-n:],
            first_page_idx=len(self.pages) - n,
        )

    def get_range(self, start, end):
        return self.pages[start:end]


class Db:

    def __init__(self):
        self.reloadable_state = ReloadableState(
            last_id=None,
            unsaved_pages=None
        )
        self.rooms = {}

    def create_room(self, time, room_id):
        if room_id in self.rooms:
            raise RoomExistsException("[DbMock] room '" + room_id +
                                      "' already exists")
        self.rooms[room_id] = DbRoom(room_id)

    def delete_room(self, room_id):
        if not room_id in self.rooms:
            raise RoomDoesntExistException("[DbMock] room '" + room_id +
                                           "' doesnt exist")
        self.rooms.pop(room_id)

    def get_room(self, room_id) -> DbRoom:
        if not room_id in self.rooms:
            raise RoomDoesntExistException("[DbMock] room '" + room_id +
                                           "' doesn't exist")
        return self.rooms[room_id]

    def get_restart_data(self):
        res = []
        for room_id in self.rooms:
            r = self.rooms[room_id]
            res.append(RoomRestartData(
                room_id=room_id,
                name=r.name,
                pages_n=len(r.pages),
            ))
        return res

    def set_reloadable_state(self, last_id, unsaved_pages):
        self.reloadable_state = ReloadableState(
            last_id=last_id,
            unsaved_pages=unsaved_pages
        )

    def get_reloadable_state(self):
        return self.reloadable_state


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
