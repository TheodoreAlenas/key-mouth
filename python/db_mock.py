
# License at the bottom

from db_exceptions import RoomExistsException, RoomDoesntExistException


class RoomMoments:

    def __init__(self, last_moment_time, room_id, moments):
        self.last_moment_time = last_moment_time
        self.room_id = room_id
        self.name = None
        self.moments = moments

    def rename(self, name):
        self.name = name

    def add_moment(self, time, moment):
        self.moments.append({"time": time, "diffs": moment})
        self.last_moment_time = time

    def get_last_few(self):
        m = self.moments
        return {"start": 0, "end": len(m), "moments": m}

    def get_len(self):
        return len(self.moments)

    def get_range(self, start, end):
        return self.moments[start:end]


class RoomRestartData:

    def __init__(self, room_id, name, last_moment_time):
        self.room_id = room_id
        self.name = name
        self.last_moment_time = last_moment_time


class Db:

    def __init__(self):
        self.rooms = {}

    def create_room(self, time, name):
        if name in self.rooms:
            raise RoomExistsException("[DbMoct] room '" + name +
                                      "' already exists")
        self.rooms[name] = RoomMoments(
            time, name, [{"time": time, "diffs": []}])

    def delete_room(self, name):
        if not name in self.rooms:
            raise RoomDoesntExistException("[DbMoct] room '" + name +
                                           "' doesnt exist")
        self.rooms.pop(name)

    def get_room(self, name) -> RoomMoments:
        if not name in self.rooms:
            raise RoomDoesntExistException("[DbMock] room '" + name +
                                           "' doesn't exist")
        return self.rooms[name]

    def get_restart_data(self):
        res = []
        for room_id in self.rooms:
            r = self.rooms[room_id]
            res.append(RoomRestartData(
                room_id=room_id,
                name=r.name,
                last_moment_time=r.last_moment_time))
        return res


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
