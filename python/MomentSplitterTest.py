from MomentSplitter import \
    MomentSplitter, ConfTiming, MomentSplitterData
import unittest


class MSA(unittest.TestCase):

    def setUp(self):
        conf = ConfTiming(
            min_silence=10.0,
            min_moment=1.0
        )
        room = MomentSplitterData(
            last_moment_time=10.0,
            nobody_talked_yet=True
        )
        self.s1 = MomentSplitter(conf_timing=conf, room=room)
        self.s2 = MomentSplitter(conf_timing=conf, room=room)
        self.s3 = MomentSplitter(conf_timing=conf, room=room)

    def test_update_noSplit(self):
        r = self.s1.update(10.1)
        self.assertEqual(False, r.should_split)

    def test_pauseUpdate_noSplit(self):
        r = self.s1.update(1000.0)
        self.assertEqual(False, r.should_split)

    def test_updateUpdate_noSplit(self):
        self.s1.update(10.0)
        r = self.s1.update(19.9)
        self.assertEqual(False, r.should_split)

    def test_updatePauseUpdate_split(self):
        self.s1.update(10.0)
        r = self.s1.update(20.0)
        self.assertEqual(True, r.should_split)

    def test_update1Update2_noSplit(self):
        self.s1.update(10.0)
        r = self.s2.update(10.9)
        self.assertEqual(False, r.should_split)

    def test_update1PauseUpdate2_split(self):
        self.s1.update(10.0)
        r = self.s2.update(11.0)
        self.assertEqual(True, r.should_split)

    def test_update1Update2Update3_split(self):
        self.s1.update(10.0)
        self.s2.update(10.9)
        r = self.s3.update(11.0)
        self.assertEqual(True, r.should_split)

    def test_updateUpdateUpdate_noSplit(self):
        self.s1.update(10.0)
        self.s1.update(19.9)
        r = self.s1.update(20.8)
        self.assertEqual(False, r.should_split)

    def test_first_message_advises_new_moment_event(self):
        r = self.s1.update(11.0)
        self.assertEqual(True, r.should_say_new_moment)

    def test_second_message_doesnt_advise_new_moment_event(self):
        self.s1.update(11.0)
        r = self.s1.update(20.9)
        self.assertEqual(False, r.should_say_new_moment)

    def test_split_advises_new_moment_event(self):
        self.s1.update(11.0)
        r = self.s1.update(21.0)
        self.assertEqual(True, r.should_say_new_moment)


if __name__ == "__main__":
    unittest.main()
