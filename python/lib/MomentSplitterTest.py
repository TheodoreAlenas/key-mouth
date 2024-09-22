from lib.MomentSplitter import MomentSplitter, MomentSplitterData
import unittest


class MSA(unittest.TestCase):

    def setUp(self):
        def create_splitter(room):
            return MomentSplitter(
                min_silence=10.0,
                min_moment=1.0,
                room=room,
            )
        room = MomentSplitterData()
        self.s1 = create_splitter(room)
        self.s2 = create_splitter(room)
        self.s3 = create_splitter(room)

    def test_update_noSplit(self):
        r = self.s1.get_should_split(10.1)
        self.assertEqual(False, r)

    def test_pauseUpdate_noSplit(self):
        r = self.s1.get_should_split(1000.0)
        self.assertEqual(False, r)

    def test_updateUpdate_noSplit(self):
        self.s1.get_should_split(10.0)
        r = self.s1.get_should_split(19.9)
        self.assertEqual(False, r)

    def test_updatePauseUpdate_split(self):
        self.s1.get_should_split(10.0)
        r = self.s1.get_should_split(20.0)
        self.assertEqual(True, r)

    def test_update1Update2_noSplit(self):
        self.s1.get_should_split(10.0)
        r = self.s2.get_should_split(10.9)
        self.assertEqual(False, r)

    def test_update1PauseUpdate2_split(self):
        self.s1.get_should_split(10.0)
        r = self.s2.get_should_split(11.0)
        self.assertEqual(True, r)

    def test_update1Update2Update3_split(self):
        self.s1.get_should_split(10.0)
        self.s2.get_should_split(10.9)
        r = self.s3.get_should_split(11.0)
        self.assertEqual(True, r)

    def test_updateUpdateUpdate_noSplit(self):
        self.s1.get_should_split(10.0)
        self.s1.get_should_split(19.9)
        r = self.s1.get_should_split(20.8)
        self.assertEqual(False, r)


if __name__ == "__main__":
    unittest.main()
