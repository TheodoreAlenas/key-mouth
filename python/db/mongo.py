
# License at the bottom

from db.exceptions import RoomExistsException, RoomDoesntExistException
import db.server_only_gitig
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dataclasses import dataclass


class RoomMoments:

    def __init__(self, room_id, n, last_moment_time, name, db):
        self.last_moment_time = last_moment_time
        self.n = n
        self.room_id = room_id
        self.name = name
        self._db = db

    def rename(self, name):
        self._db['rooms'].update_one(
            {'_id': self.room_id},
            {'$set': {'name': name}}
        )
        self.name = name

    def add_moment(self, moment):
        self._db['rooms'].update_one(
            {"_id": self.room_id},
            {"$push": {"moments": moment}}
        )
        self.n += 1
        self.last_moment_time = moment['time']

    def get_last_few(self):
        ms = self._db['rooms'].find_one(
            {"_id": self.room_id},
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
        ms = self._db['rooms'].find_one(
            {"_id": self.room_id},
            {"moments": {"$slice": [start, end - start]}}
        )
        return ms['moments']


@dataclass
class RoomRestartData:
    room_id: any
    name: str
    last_moment_time: float


@dataclass
class AfterSocketLogicRestartData:
    last_id: any


def delete_test_db():
    client = MongoClient(db.server_only_gitig.db_uri)
    client.drop_database('keymouthTest')


class Db:

    def __init__(self, is_test=False):
        db_name = 'keymouth'
        if is_test:
            db_name += 'Test'
        self._client = MongoClient(db.server_only_gitig.db_uri)
        self._db = self._client[db_name]
        self._rooms = {}
        projection = {
            'n': {'$size': '$moments'},
            'last': {'$arrayElemAt': ['$moments', -1]}
        }
        n_last = self._db['rooms'].aggregate([{'$project': projection}])
        names = self._db['rooms'].find({}, ['name'])
        for nl, nm in zip(n_last, names):
            name = None
            if 'name' in nm:
                name = nm['name']
            self._rooms[nl['_id']] = RoomMoments(
                room_id=nl['_id'],
                n=nl['n'],
                last_moment_time=nl['last']['time'],
                name=name,
                db=self._db
            )

    def drop_keymouth_test(self):
        self._client.drop_database('keymouthTest')

    def close(self):
        self._client.close()

    def create_room(self, time, room_id):
        try:
            room = RoomMoments(
                room_id=room_id,
                n=0,
                last_moment_time=time,
                name=None,
                db=self._db
            )
            self._db['rooms'].insert_one({
                "_id": room_id,
                "moments": []
            })
            self._rooms[room_id] = room
        except DuplicateKeyError:
            raise RoomExistsException("[Db] room '" + name +
                                      "' already exists")

    def delete_room(self, room_id):
        try:
            if not room_id in self._rooms:
                raise RoomDoesntExistException("")
            self._db['rooms'].delete_one({'_id': room_id})
            self._rooms.pop(room_id)
        except Exception as e:
            raise RoomDoesntExistException(
                "[Db] room '" + room_id + "' doesn't exist,\n" +
                e.message
            )

    def get_room(self, name) -> RoomMoments:
        if not name in self._rooms:
            raise RoomDoesntExistException("[DbMock] room '" + name +
                                           "' doesn't exist")
        return self._rooms[name]

    def get_restart_data(self):
        res = []
        for room_id in self._rooms:
            r = self._rooms[room_id]
            res.append(RoomRestartData(
                room_id=room_id,
                name=r.name,
                last_moment_time=r.last_moment_time
            ))
        return res

    def save_state(self, last_id):
        r = self._db['reloadableState'].update_one(
            {}, {"$set": {'lastId': last_id}})
        if r.modified_count != 1:
            self._db['reloadableState'].insert_one(
                {'lastId': last_id})

    def reload_state(self):
        s = self._db['reloadableState'].find_one({})
        if s is None:
            return None
        return AfterSocketLogicRestartData(last_id=s['lastId'])


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
