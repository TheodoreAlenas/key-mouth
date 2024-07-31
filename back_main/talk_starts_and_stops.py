import unittest

def talk_starts_and_stops(actions, min_pause):
    if len(actions) < 2:
        return []
    timestamps = []
    last = {actions[0]["user"]: actions[0]["time"]}
    for i in range(1, len(actions)):
        u1 = actions[i]["user"]
        t1 = actions[i]["time"]
        t0 = last[actions[i-1]["user"]]
        if u1 in last.keys():
            if t1 - t0 >= min_pause:
                timestamps.append(t1)
        elif len(last) > 0:
            timestamps.append(t1)
        last[u1] = t1
    return timestamps


class TestTalkStartsAndStops(unittest.TestCase):

    def test_0_or_1_messages_no_timestamps(self):
        self.assertEqual([], talk_starts_and_stops([{}], 1.0))
        self.assertEqual([], talk_starts_and_stops(
            [{"user": 0, "time": 0.0}], 1.0))

    def test_two_slow_messages_timestamp_on_second(self):
        self.assertEqual([1.1], talk_starts_and_stops(
            [{"user": 0, "time": 0.0},
             {"user": 0, "time": 1.1}], 1.0))

    def test_two_fast_messages_no_timestamps(self):
        self.assertEqual([], talk_starts_and_stops(
            [{"user": 0, "time": 0.0},
             {"user": 0, "time": 0.9}], 1.0))

    def test_two_fast_one_slow_stamps_last(self):
        self.assertEqual([2.0], talk_starts_and_stops(
            [{"user": 0, "time": 0.0},
             {"user": 0, "time": 0.9},
             {"user": 0, "time": 2.0}], 1.0))

    def test_interrupting_user_gets_timestamp(self):
        self.assertEqual([0.1], talk_starts_and_stops(
            [{"user": 0, "time": 0.0},
             {"user": 1, "time": 0.1}], 1.0))

    def test_interrupting_user_gets_timestamp(self):
        self.assertEqual([0.1], talk_starts_and_stops(
            [{"user": 0, "time": 0.0},
             {"user": 1, "time": 0.1}], 1.0))


if __name__ == "__main__":
    unittest.main()
