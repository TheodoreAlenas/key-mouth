from Rooms import Rooms
from db.mock import Db
from db.exceptions import RoomExistsException, RoomDoesntExistException
from exceptions import LogicHttpException
import unittest


class RA(unittest.TestCase):

    def setUp(self):
        self.rooms = Rooms(10.0, Db(), [])

    def test_init_no_rooms(self):
        self.assertEqual(0, len(self.rooms.get_all()))

    def test_deleted_room_not_listed(self):
        self.rooms.create(10.0, "room0")
        self.rooms.delete("room0")
        self.assertEqual(0, len(self.rooms.get_all()))

    def test_created_room_listed(self):
        self.rooms.create(10.0, "room0")
        self.assertEqual(1, len(self.rooms.get_all()))
        self.assertEqual("room0", self.rooms.get_all()[0].room_id)
        self.assertEqual(None, self.rooms.get_all()[0].name)

    def test_renamed_room_listed_renamed(self):
        self.rooms.create(10.0, "room0")
        self.rooms.rename("room0", "a name")
        self.assertEqual(1, len(self.rooms.get_all()))
        self.assertEqual("room0", self.rooms.get_all()[0].room_id)
        self.assertEqual("a name", self.rooms.get_all()[0].name)

    def assertStatusCode(self, status_code, f):
        try:
            f()
            self.assertFalse("should have thrown error")
        except LogicHttpException as e:
            self.assertEqual(status_code, e.status_code)

    def test_create_room_twice_get_409(self):
        def t():
            self.rooms.create(10.0, "room0")
            self.rooms.create(10.1, "room0")
        self.assertStatusCode(409, t)

    def test_delete_nonexistent_get_404(self):
        def t():
            self.rooms.delete("nonexistent")
        self.assertStatusCode(404, t)

    def test_without_existing_get_409(self):
        self.rooms.create(10.0, "existing")
        def f():
            pass
        def t():
            self.rooms.without("existing", f)
        self.assertStatusCode(409, t)

    def test_given_nonexistent_get_404(self):
        def f(_):
            pass
        def t():
            self.rooms.given("nonexistent", f)
        self.assertStatusCode(404, t)

    def test_in_without_inner_raises_get_409(self):
        def f():
            raise RoomExistsException()
        def t():
            self.rooms.without("nonexistent", f)
        self.assertStatusCode(409, t)

    def test_in_without_inner_errors_reraise(self):
        class CustomException(Exception):
            pass
        def f():
            raise CustomException()
        def t():
            self.rooms.without("nonexistent", f)
        self.assertRaises(CustomException, f)

    def test_in_given_inner_raises_get_404(self):
        self.rooms.create(10.0, "existing")
        def f(_):
            raise RoomDoesntExistException()
        def t():
            self.rooms.given("existing", f)
        self.assertStatusCode(404, t)

    def test_in_given_inner_errors_reraise(self):
        class CustomException(Exception):
            pass
        self.rooms.create(10.0, "existing")
        def f(_):
            raise CustomException()
        def t():
            self.rooms.given("existing", f)
        self.assertRaises(CustomException, t)


if __name__ == "__main__":
    unittest.main()
