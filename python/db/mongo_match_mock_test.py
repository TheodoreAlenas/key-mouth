import db.mock
import db.mongo
import unittest


class BothRooms:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def rename(self, name):
        self.a.rename(name)
        self.b.rename(name)

    def add_moment(self, moment):
        self.a.add_moment(moment)
        self.b.add_moment(moment)

    def get_last_few(self):
        return (self.a.get_last_few(),
                self.b.get_last_few())

    def get_len(self):
        return (self.a.get_len(),
                self.b.get_len())

    def get_range(self, start, end):
        return (self.a.get_range(start, end),
                self.b.get_range(start, end))


def obj_to_dict(o):
    d = {}
    for e in dir(o):
        if e[0] == '_':
            continue
        d[e] = o.__getattribute__(e)
    return d


class BothDbs:

    def __init__(self):
        self.real = db.mongo.Db(is_test=True)
        self.mock = db.mock.Db()

    def create_room(self, time, name):
        self.real.create_room(time, name)
        self.mock.create_room(time, name)

    def delete_room(self, name):
        self.real.delete_room(name)
        self.mock.delete_room(name)

    def get_room(self, name):
        a = self.real.get_room(name)
        b = self.mock.get_room(name)
        return BothRooms(a, b)

    def get_restart_data(self):
        a = self.real.get_restart_data()
        b = self.mock.get_restart_data()
        return ([obj_to_dict(o) for o in a],
                [obj_to_dict(o) for o in b])


class A(unittest.TestCase):

    def setUp(self):
        self.dbs = BothDbs()

    def tearDown(self):
        self.dbs.real.drop_keymouth_test()
        self.dbs.real.close()

    def test_just_get_restart_data(self):
        a, b = self.dbs.get_restart_data()
        self.assertEqual(a, b)

    def test_create_and_get_restart_data(self):
        self.dbs.create_room(10.0, "thanasis")
        a, b = self.dbs.get_restart_data()
        self.assertEqual(a, b)

    def test_create_delete_and_get_restart_data(self):
        self.dbs.create_room(10.0, "thanasis")
        self.dbs.delete_room("thanasis")
        a, b = self.dbs.get_restart_data()
        self.assertEqual(a, b)

    def test_create_create_delete_and_get_restart_data(self):
        self.dbs.create_room(10.0, "thanasis")
        self.dbs.create_room(12.0, "vaggas")
        self.dbs.delete_room("thanasis")
        a, b = self.dbs.get_restart_data()
        self.assertEqual(a, b)

    def test_create_get_rename_getrestartdata(self):
        self.dbs.create_room(10.0, "thanasis")
        rooms = self.dbs.get_room("thanasis")
        rooms.rename("vaggas")
        a, b = self.dbs.get_restart_data()
        self.assertEqual(a, b)

    def test_create_get_getlastfew(self):
        self.dbs.create_room(10.0, "thanasis")
        rooms = self.dbs.get_room("thanasis")
        a, b = rooms.get_last_few()
        self.assertEqual(a, b)

    def test_create_get_getlen(self):
        self.dbs.create_room(10.0, "thanasis")
        rooms = self.dbs.get_room("thanasis")
        a, b = rooms.get_len()
        self.assertEqual(a, b)

    def test_create_get_addmoment_get(self):
        self.dbs.create_room(10.0, "thanasis")
        rooms = self.dbs.get_room("thanasis")
        rooms.add_moment({'time': 11.0, 'diffs': ['whatever']})
        a, b = rooms.get_last_few()
        self.assertEqual(a, b)
        a, b = rooms.get_len()
        self.assertEqual(a, b)
        a, b = rooms.get_range(0, 1)
        self.assertEqual(a, b)

    def test_add_3_moments_get_ranges(self):
        self.dbs.create_room(10.0, "thanasis")
        rooms = self.dbs.get_room("thanasis")
        rooms.add_moment({'time': 101.0, 'diffs': [10]})
        rooms.add_moment({'time': 102.0, 'diffs': [20]})
        rooms.add_moment({'time': 103.0, 'diffs': [30]})
        a, b = rooms.get_range(0, 1)
        self.assertEqual(a, b)
        a, b = rooms.get_range(1, 2)
        self.assertEqual(a, b)
        a, b = rooms.get_range(0, 2)
        self.assertEqual(a, b)


class B(unittest.TestCase):

    def setUp(self):
        self.db = db.mongo.Db(is_test=True)

    def tearDown(self):
        self.db.drop_keymouth_test()
        self.db.close()

    def test_reopen_same_outputs(self):

        for room_id, name in [(f"id{x}", f"nm{x}") for x in range(30)]:
            self.db.create_room(10.0, room_id)
            room = self.db.get_room(room_id)
            room.rename(name)

        a = self.db.get_restart_data()
        self.db.close()
        self.db = db.mongo.Db(is_test=True)
        b = self.db.get_restart_data()

        self.assertEqual([obj_to_dict(x) for x in a],
                         [obj_to_dict(x) for x in b])
