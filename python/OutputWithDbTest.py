from OutputWithDb import OutputWithDb
import unittest


class Db:

    def __init__(self):
        self.s = []

    def get_len(self):
        return len(self.s)

    def add_moment(self, moment):
        self.s.append(moment)

    def get_last_few(self):
        return {'start': 0, 'end': len(self.s), 'moments': self.s}


class A(unittest.TestCase):

    def setUp(self):
        self.db = Db()
        self.o = OutputWithDb(Db())

    def test_push_store_get(self):
        a = []
        a.append(self.o.push(0, 'newMoment', 10.0))
        a.append(self.o.push(1, 'write', 'hello'))
        self.o.store_last_moment(11.0)
        b = self.o.get_last_few()['moments']
        self.assertEqual(a, b)

    def test_push_store_push_store_get(self):
        a = []
        a.append(self.o.push(0, 'newMoment', 10.0))
        a.append(self.o.push(1, 'write', 'a'))
        self.o.store_last_moment(11.0)
        a.append(self.o.push(0, 'newMoment', 10.0))
        a.append(self.o.push(1, 'write', 'b'))
        self.o.store_last_moment(12.0)
        b = self.o.get_last_few()['moments']
        self.assertEqual(a, b)

    def test_push_push_store_get(self):
        a = []
        a.append(self.o.push(0, 'newMoment', 10.0))
        a.append(self.o.push(1, 'write', 'a'))
        a.append(self.o.push(1, 'write', 'b'))
        self.o.store_last_moment(12.0)
        b = self.o.get_last_few()['moments']
        self.assertEqual(a, b)
