from lib.PersistentOutputMapper import PersistentOutputMapper
from db.mock import Db
import unittest


class A(unittest.TestCase):

    def setUp(self):
        db = Db()
        db.create_room(time=100, room_id="room0")
        room = db.get_room(room_id="room0")
        self.o = PersistentOutputMapper(
            db=room,
            next_moment_idx=0,
            unsaved_page=None,
            debug_context_str='unit test',
        )
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

    def test_push_store_push_store_get_ranges(self):
        self.o.save_last_page()
        c0 = self.o.get_pages_range(0, 1)
        self.assertEqual(self.a, c0)
        self.a.append(self.o.push(0, 'newPage', 1))
        self.a.append(self.o.push(0, 'newMoment', 10.0))
        self.a.append(self.o.push(1, 'write', 'b'))
        self.o.save_last_page()
        c1 = self.o.get_pages_range(0, 1)
        c2 = self.o.get_pages_range(1, 2)
        self.assertEqual(c0, c1)
        self.assertEqual(c1 + c2, self.a)
        c = self.o.get_pages_range(0, 2)
        self.assertEqual(c, self.a)


if __name__ == "__main__":
    unittest.main()
