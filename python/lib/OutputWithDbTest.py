from lib.OutputWithDb import OutputWithDb
from db.mock import Db
import unittest


class A(unittest.TestCase):

    def setUp(self):
        db = Db()
        db.create_room(time=100, room_id="room0")
        room = db.get_room(room_id="room0")
        self.o = OutputWithDb(db=room)
        self.a = []
        self.a.append(self.o.push(0, 'newPage', 0))
        self.a.append(self.o.push(0, 'newMoment', 10.0))
        self.a.append(self.o.push(1, 'write', 'a'))

    def test_push_store_get(self):
        self.o.save_last_page()
        b = self.o.get_last_pages()['events']
        self.assertEqual(self.a, b)

    def test_push_store_push_store_get(self):
        self.o.save_last_page()
        self.a.append(self.o.push(0, 'newPage', 1))
        self.a.append(self.o.push(0, 'newMoment', 10.0))
        self.a.append(self.o.push(1, 'write', 'b'))
        self.o.save_last_page()
        b = self.o.get_last_pages()['events']
        self.assertEqual(self.a, b)

    def test_push_push_store_get(self):
        self.a.append(self.o.push(1, 'write', 'b'))
        self.o.save_last_page()
        b = self.o.get_last_pages()['events']
        self.assertEqual(self.a, b)


if __name__ == "__main__":
    unittest.main()
