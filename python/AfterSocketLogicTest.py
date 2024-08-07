from AfterSocketLogic import AfterSocketLogic, AfterSocketPublicLogic, Moments
import unittest


class AfterSocketLogicTest(unittest.TestCase):

    def setUp(self):
        self.logic = AfterSocketPublicLogic(AfterSocketLogic(
            8.0, Moments(9.0), min_silence=3.0, min_moment=0.5))
        self.logic.create_room(10.0, "room0")
        self.logic.create_room(10.0, "room1")

    def test_one_conn_one_msg(self):
        _, conn = self.logic.connect(10.0, "room0")
        res, _ = conn.handle_input(10.1, "+")
        self.assertEqual([], res)
        res, _ = conn.handle_input(10.2, "hello")
        self.assertEqual(
            [(
                conn.conn_id,
                {"lastMoment": [], "curMoment": [{
                    "connId": conn.conn_id,
                    "type": "write",
                    "body": "hello"}]}
            )],
            res)

    def test_two_conn_one_msg_bcast(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(11.0, "room0")
        conn_1.handle_input(12.0, "+")
        res, _ = conn_1.handle_input(13.0, "hello")
        self.assertEqual(2, len(res))
        self.assertEqual(res[0][1], res[1][1])
        a = [conn_1.conn_id, conn_2.conn_id]
        b = [res[0][0], res[1][0]]
        a.sort()
        b.sort()
        self.assertEqual(a, b)

    def test_a_comes_b_comes_a_goes_one_msg(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(11.0, "room0")
        conn_1.disconnect(12.0, None)
        conn_2.handle_input(12.0, "+")
        res, _ = conn_2.handle_input(13.0, "hello")
        self.assertEqual(1, len(res))
        self.assertEqual(conn_2.conn_id, res[0][0])

    #def test_two_conn_one_msg_each_and_last_goes_last(self):
    #    _, conn_1 = self.logic.connect(10.0, "room0")
    #    _, conn_2 = self.logic.connect(11.0, "room0")
    #    conn_1.handle_input(         11.0, "+")
    #    conn_2.handle_input(         12.0, "+")
    #    conn_2.handle_input(         13.0, "2")
    #    res, _ = conn_1.handle_input(14.0, "1")
    #    self.assertEqual(
    #        [
    #            {"connId": conn_2.conn_id, "type": "write", "body": "2"},
    #            {"connId": conn_1.conn_id, "type": "write", "body": "1"}
    #        ],
    #        res[0][1]["curMoment"])
    #    self.assertEqual(res[0][1], res[1][1])

    def test_message_in_one_room_is_isolated(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(11.0, "room1")
        conn_1.handle_input(12.0, "+")
        res, _ = conn_1.handle_input(13.0, "1")
        self.assertEqual(1, len(res))

    def test_create_room_twice_get_409(self):
        try:
            self.logic.create_room(10.0, "room0")
            self.assertFalse("should have thrown error")
        except Exception as e:
            self.assertEqual(409, e.status_code)

    def test_connect_get_no_moments(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res, _ = conn_1.update(10.1, None)
        self.assertEqual(None, res[0][1]["lastMoment"])

    def test_interrupting_creates_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(10.2, "+")
        before, _ = conn_1.handle_input(10.3, "1")
        conn_2.handle_input(11.2, "+")
        after, _ = conn_2.handle_input(11.3, "2")
        self.assertEqual(
            before[0][1]["curMoment"], after[0][1]["lastMoment"])
        self.assertEqual(1, len(after[0][1]["curMoment"]))

    def test_last_moment_notification_resets(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(10.2, "+")
        conn_1.handle_input(10.3, "1")
        conn_2.handle_input(11.2, "+")
        conn_2.handle_input(11.3, "2")
        conn_2.handle_input(11.4, "+")
        res, _ = conn_2.handle_input(11.5, "2")
        self.assertEqual(None, res[0][1]["lastMoment"])

    def test_nearby_moments_merge(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(10.2, "+")
        conn_1.handle_input(10.3, "1")
        conn_2.handle_input(10.6, "+")
        res, _ = conn_2.handle_input(10.7, "2")
        self.assertEqual(None, res[0][1]["lastMoment"])

    def test_database_starts_empty(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        conn_1.handle_input(10.1, "+")
        res, _ = self.logic.get_last_few(10.2, "room0")
        self.assertEqual([], res)

    def test_database_reflects_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        conn_1.handle_input(10.1, "+")
        res, _ = conn_1.handle_input(10.1, "hello")
        self.assertEqual([], res[0][1]["lastMoment"])
        _, last_few = self.logic.get_last_few(10.2, "room0")
        self.assertEqual([[]], last_few)


if __name__ == "__main__":
    unittest.main()
