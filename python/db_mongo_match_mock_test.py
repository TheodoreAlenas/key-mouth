import db_mock
import db_mongo
import server_only
import unittest


class BothRooms:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def rename(self, name):
        self.a.rename(name)
        self.b.rename(name)

    def add_moment(self, time, moment):
        self.a.add_moment(time, moment)
        self.b.add_moment(time, moment)

    def get_last_few(self):
        return (self.a.get_last_few(),
                self.b.get_last_few())

    def get_len(self):
        return (self.a.get_len(),
                self.b.get_len())

    def get_range(self, start, end):
        return (self.a.get_range(start, end),
                self.b.get_range(start, end))


class BothDbs:

    def __init__(self):
        self.db_real = db_mongo.Db(is_test=True)
        self.db_mock = db_mock.Db()

    def drop_keymouth_test(self):
        self.db_real.drop_keymouth_test()

    def create_room(self, time, name):
        self.db_real.create_room(time, name)
        self.db_mock.create_room(time, name)

    def delete_room(self, name):
        self.db_real.delete_room(name)
        self.db_mock.delete_room(name)

    def get_room(self, name):
        a = self.db_real.get_room(name)
        b = self.db_mock.get_room(name)
        return BothRooms(a, b)

    def get_restart_data(self):
        return (self.db_real.get_restart_data(),
                self.db_mock.get_restart_data())


class A(unittest.TestCase):

    def setUp(self):
        self.dbs = BothDbs()

    def tearDown(self):
        self.dbs.drop_keymouth_test()

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
        rooms.add_moment(11.0, ['whatever'])
        a, b = rooms.get_last_few()
        self.assertEqual(a, b)
        a, b = rooms.get_len()
        self.assertEqual(a, b)
        a, b = rooms.get_range(0, 1)
        self.assertEqual(a, b)

    def test_add_3_moments_get_ranges(self):
        self.dbs.create_room(10.0, "thanasis")
        rooms = self.dbs.get_room("thanasis")
        rooms.add_moment(101.0, [10])
        rooms.add_moment(102.0, [20])
        rooms.add_moment(103.0, [30])
        a, b = rooms.get_range(0, 0)
        self.assertEqual(a, b)
        a, b = rooms.get_range(0, 1)
        self.assertEqual(a, b)
        a, b = rooms.get_range(1, 1)
        self.assertEqual(a, b)
        a, b = rooms.get_range(1, 2)
        self.assertEqual(a, b)
        a, b = rooms.get_range(0, 2)
        self.assertEqual(a, b)
        a, b = rooms.get_range(2, 1)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
