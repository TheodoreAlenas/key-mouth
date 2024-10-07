
# License at the bottom

from db.exceptions import RoomExistsException, RoomDoesntExistException
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dataclasses import dataclass
from os import environ


DB_URI = environ['KEYMOUTH_DB']


@dataclass
class LastPages:
    pages: list
    first_page_idx: int
    first_moment_idx: int


class DbRoom:

    def __init__(self, room_id, db):
        self.room_id = room_id
        self._db = db

    def rename(self, name):
        self._db.update_one(
            {'_id': self.room_id},
            {'$set': {'name': name}}
        )

    def push_page(self, page):
        self._db.update_one(
            {"_id": self.room_id},
            {"$push": {"pages": page}}
        )

    def get_last_pages(self, n):
        r = self._db.find_one(
            {"_id": self.room_id},
            {
                "pages": {"$slice": [-n, n]},
                "n": {"$size": "$pages"},
            }
        )
        return LastPages(
            pages=r['pages'],
            first_page_idx=r['n'] - len(r['pages'])
        )

    def get_len(self):
        return self.pages_n

    def get_range(self, start, end):
        ms = self._db.find_one(
            {"_id": self.room_id},
            {"pages": {"$slice": [start, end - start]}}
        )
        return ms['pages']


@dataclass
class RoomRestartData:
    room_id: any
    name: str
    last_page_first_moment_idx: int
    pages_n: int


@dataclass
class ReloadableState:
    last_id: any
    unsaved_pages: dict | None


def delete_test_db():
    client = MongoClient(DB_URI)
    client.drop_database('keymouthTest')


class Db:

    def __init__(self, is_test=False):
        db_name = 'keymouth'
        if is_test:
            db_name += 'Test'
        self._client = MongoClient(DB_URI)
        self._db = self._client[db_name]
        self._rooms = {}
        results = self._db['rooms'].find({}, ['name'])
        for r in results:
            self._rooms[r['_id']] = DbRoom(
                room_id=r['_id'],
                name=r['name'] if 'name' in r else None,
                db=self._db['rooms'],
            )

    def drop_keymouth_test(self):
        self._client.drop_database('keymouthTest')

    def close(self):
        self._client.close()

    def create_room(self, time, room_id):
        try:
            room = DbRoom(
                room_id=room_id,
                db=self._db['rooms'],
            )
            self._db['rooms'].insert_one({
                "_id": room_id,
                "pages": []
            })
            self._rooms[room_id] = room
        except DuplicateKeyError:
            raise RoomExistsException("[Db] room '" + name +
                                      "' already exists")

    def delete_room(self, room_id):
        try:
            if not room_id in self._rooms:
                raise RoomDoesntExistException("not found in RAM")
            self._db['rooms'].delete_one({'_id': room_id})
            self._rooms.pop(room_id)
        except Exception as e:
            raise RoomDoesntExistException(
                "[Db] room '" + room_id + "' doesn't exist,\n" +
                e.message
            )

    def get_room(self, name) -> DbRoom:
        if not name in self._rooms:
            raise RoomDoesntExistException("[Db] room '" + name +
                                           "' not found in RAM")
        return self._rooms[name]

    def get_restart_data(self):
        res = []
        names = self._db['rooms'].find({}, ['name'])
        ns = self._db['rooms'].aggregate([{
            '$project': {'n': {'$size': '$moments'}}
        }])
        for name, n in zip(names, ns):
            res.append(RoomRestartData(
                room_id=name['_id'],
                name=name['name'],
                pages_n=n['n'],
            ))
        return res

    def set_reloadable_state(self, last_id, unsaved_pages):
        d = {
            'lastId': last_id,
            'unsavedPages': unsaved_pages,
        }
        r = self._db['reloadableState'].update_one({}, {"$set": d})
        if r.modified_count != 1:
            self._db['reloadableState'].insert_one(d)

    def get_reloadable_state(self):
        s = self._db['reloadableState'].find_one({})
        if s is None:
            return None
        return ReloadableState(
            last_id=s['lastId'],
            unsaved_pages=s['unsavedPages'],
        )


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
