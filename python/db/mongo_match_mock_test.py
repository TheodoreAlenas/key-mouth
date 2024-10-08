import db.mock
import db.mongo
import unittest
from db.exceptions import RoomExistsException, RoomDoesntExistException


def both(a, b, f, args, kwargs):
    aret = a.__getattribute__(f)(*args, **kwargs)
    bret = b.__getattribute__(f)(*args, **kwargs)
    return (aret, bret)


class BothRooms:

    def __init__(self, real, mock):
        self.real = real
        self.mock = mock

    def __getattr__(self, name):
        def f(*args, **kwargs):
            return both(self.real, self.mock, name, args, kwargs)
        return f


class BothDbs:

    def __init__(self):
        self.real = db.mongo.Db(is_test=True)
        self.mock = db.mock.Db()

    def __getattr__(self, name):
        def f(*args, **kwargs):
            return both(self.real, self.mock, name, args, kwargs)
        return f


def before_main():
    db.mongo.delete_test_db()


class A(unittest.TestCase):

    def setUp(self):
        self.dbs = BothDbs()

    def tearDown(self):
        self.dbs.real.drop_keymouth_test()
        self.dbs.real.close()

    def dbs_get_room(self, name):
        real, mock = self.dbs.get_room(room_id=name)
        return BothRooms(real=real, mock=mock)

    def assertBothRaise(self, exc, real, mock, name, args, kwargs):
        def real_f():
            real.__getattribute__(name)(*args, **kwargs)
        def mock_f():
            mock.__getattribute__(name)(*args, **kwargs)
        self.assertRaises(exc, real_f)
        self.assertRaises(exc, mock_f)

    def test_empty(self):
        self.assertEqual(*self.dbs.get_restart_data())
        self.assertBothRaise(
            RoomDoesntExistException,
            real=self.dbs.real,
            mock=self.dbs.mock,
            name='get_room',
            args=("doesntexist",),
            kwargs=dict(),
        )

    def test_create_delete(self):
        self.assertEqual(*self.dbs.create_room(time=10.0,
                                               room_id="thana sis"))
        self.assertEqual(*self.dbs.get_restart_data())
        self.assertBothRaise(
            RoomExistsException,
            real=self.dbs.real,
            mock=self.dbs.mock,
            name='create_room',
            args=tuple(),
            kwargs={'time': 11.0, 'room_id': "thana sis"},
        )
        self.assertEqual(*self.dbs.get_restart_data())
        self.assertEqual(*self.dbs.delete_room(room_id="thana sis"))
        self.assertEqual(*self.dbs.get_restart_data())

    def test_create_and_get_restart_data(self):

        self.assertEqual(*self.dbs.get_restart_data())

        self.assertEqual(*self.dbs.create_room(11.0, "thanasis"))
        self.assertEqual(*self.dbs.delete_room("thanasis"))
        self.assertEqual(*self.dbs.get_restart_data())

        self.assertEqual(*self.dbs.create_room(12.0, "thanasis"))
        self.assertEqual(*self.dbs.create_room(13.0, "vaggas"))
        self.assertEqual(*self.dbs.delete_room("thanasis"))
        self.assertEqual(*self.dbs.get_restart_data())
        self.assertEqual(*self.dbs.delete_room("vaggas"))
        self.assertEqual(*self.dbs.get_restart_data())

    def test_rename_and_get_last_pages_on_empty(self):
        self.assertEqual(*self.dbs.create_room(10.0, "thanasis"))
        rooms = self.dbs_get_room("thanasis")
        self.assertEqual(*rooms.get_last_pages(n=1))
        self.assertEqual(*self.dbs.get_restart_data())
        self.assertEqual(*rooms.rename("vaggas"))
        self.assertEqual(*self.dbs.get_restart_data())
        self.assertEqual(*rooms.get_last_pages(n=1))

        self.assertEqual(*self.dbs.create_room(11.0, "a"))
        self.assertEqual(*self.dbs.create_room(12.0, "b"))
        self.assertEqual(*self.dbs.get_restart_data())
        rooms = self.dbs_get_room("a")
        self.assertEqual(*rooms.rename("room named a"))
        self.assertEqual(*self.dbs.get_restart_data())

    def test_save_pages(self):
        self.assertEqual(*self.dbs.create_room(10.0, "thanasis"))
        self.assertEqual(*self.dbs.create_room(11.0, "vaggas"))
        rooms = self.dbs_get_room("thanasis")

        self.assertEqual(*rooms.push_page({"firstMomentIdx": 732, "a": "b"}))
        self.assertEqual(*rooms.get_last_pages(n=1))
        self.assertEqual(*rooms.get_last_pages(n=2))
        self.assertEqual(*rooms.get_range(0, 1))

        self.assertEqual(*rooms.push_page({"firstMomentIdx": 1024}))
        self.assertEqual(*rooms.get_last_pages(n=1))
        self.assertEqual(*rooms.get_last_pages(n=2))
        self.assertEqual(*rooms.get_last_pages(n=3))
        self.assertEqual(*rooms.get_range(0, 1))
        self.assertEqual(*rooms.get_range(1, 2))
        self.assertEqual(*rooms.get_range(0, 2))

        self.assertEqual(*rooms.get_range(0, 3))
        self.assertEqual(*rooms.get_range(2, 3))

        rooms = self.dbs_get_room("vaggas")
        self.assertEqual(*rooms.get_last_pages(n=1))
        self.assertEqual(*rooms.get_last_pages(n=2))

        self.assertEqual(*self.dbs.delete_room("thanasis"))
        self.assertEqual(*self.dbs.get_restart_data())
        self.assertEqual(*self.dbs.delete_room("vaggas"))
        self.assertEqual(*self.dbs.get_restart_data())

    def test_reloads(self):
        self.assertEqual(*self.dbs.get_reloadable_state())
        self.assertEqual(*self.dbs.set_reloadable_state(
            last_id=732,
            unsaved_pages=[1, 2, 3]
        ))
        self.assertEqual(*self.dbs.get_reloadable_state())
        self.assertEqual(*self.dbs.set_reloadable_state(
            last_id=0,
            unsaved_pages=[]
        ))
        self.assertEqual(*self.dbs.get_reloadable_state())
