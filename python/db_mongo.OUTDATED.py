
# License at the bottom

from db_exceptions import RoomExistsException, RoomDoesntExistException
import server_only
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class RoomMoments:

    def __init__(self, r, db):
        self._cached_last_moment = r['last']
        self.last_moment_time = r['last']['time']
        self.n = r['n']
        self.name = r['_id']
        self._db = db

    def add_moment(self, time, moment):
        mom = {"time": time, "diffs": moment}
        self._db['rooms'].update_one(
            {"_id": self.name},
            {"$push": {"moments": mom}}
        )
        self.n += 1
        self.last_moment_time = time
        self._cached_last_moment = mom

    def get_last_few(self):
        ms = self._db['rooms'].find_one(
            {"_id": self.name},
            {"moments": {"$slice": [-30, 30]}}
        )
        m = ms['moments']
        return {
            "start": self.n - len(m),
            "end": self.n,
            "moments": m
        }

    def get_len(self):
        return self.n

    def get_range(self, start, end):
        if start == self.n - 1 and end == self.n:
            return [self._cached_last_moment]
        ms = self._db['rooms'].find_one(
            {"_id": self.name},
            {"moments": {"$slice": [start, end - start]}}
        )
        return ms['moments']


class Db:

    def __init__(self, is_test=False):
        db_name = 'keymouth'
        if is_test:
            db_name += 'Test'
        self._client = MongoClient(server_only.db_uri)
        self._db = self._client[db_name]
        self._rooms = {}
        projection = {
            'n': {'$size': '$moments'},
            'last': {'$arrayElemAt': ['$moments', -1]}
        }
        rs = self._db['rooms'].aggregate([{'$project': projection}])
        for r in rs:
            self._rooms[r['_id']] = RoomMoments(r=r, db=self._db)

    def drop_keymouth_test(self):
        self._client.drop_db('keymouthTest')
        self._client.close()

    def create_room(self, time, name):
        try:
            first_moment = {"time": time, "diffs": []}
            room = RoomMoments(
                r={'_id': name, 'last': first_moment, 'n': 1},
                db=self._db
            )
            self._db['rooms'].insert_one({
                "_id": name,
                "moments": [first_moment]
            })
            self._rooms[name] = room
        except DuplicateKeyError:
            raise RoomExistsException("[Db] room '" + name +
                                      "' already exists")

    def delete_room(self, name):
        try:
            if not name in self._rooms:
                raise RoomDoesntExistException("")
            self._db['rooms'].drop_collection(name)
            self._rooms.pop(name)
        except Exception:
            raise RoomDoesntExistException(
                "[Db] room '" + name + "' doesn't exist")

    def get_room(self, name) -> RoomMoments:
        if not name in self._rooms:
            raise RoomDoesntExistException("[DbMock] room '" + name +
                                           "' doesn't exist")
        return self._rooms[name]

    def get_rooms_and_their_last_moment_times(self):
        res = []
        for name in self._rooms:
            res.append((name, self._rooms[name].last_moment_time))
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
