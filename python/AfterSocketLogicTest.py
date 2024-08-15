from AfterSocketLogic import AfterSocketLogic, AfterSocketPublicLogic, DbMock, ConfTiming
import unittest


class AfterSocketLogicTest(unittest.TestCase):

    def setUp(self):
        self.logic = AfterSocketPublicLogic(AfterSocketLogic(
            time=8.0,
            db=DbMock(),
            conf_timing=ConfTiming(
                min_silence=3.0,
                min_moment=0.5
            )))
        self.logic.create_room(10.0, "room0")
        self.logic.create_room(10.0, "room1")

    def test_one_conn_one_msg(self):
        _, conn = self.logic.connect(10.0, "room0")
        res, _ = conn.handle_input(10.1, "+hello")
        self.assertEqual(
            [(
                conn.conn_id,
                {"n": 1, "last": [{
                    "connId": conn.conn_id,
                    "type": "write",
                    "body": "hello"}]}
            )],
            res)

    def test_deletion_parsed(self):
        _, conn = self.logic.connect(10.0, "room0")
        res, _ = conn.handle_input(10.1, "-a")
        self.assertEqual([{
            "connId": conn.conn_id,
            "type": "delete",
            "body": "a"
        }], res[0][1]["last"])

    def test_two_conn_one_speaks_they_hear_the_same(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(11.0, "room0")
        res, _ = conn_1.handle_input(12.0, "+hello")
        self.assertEqual(res[0][1], res[1][1])

    def test_two_conn_one_speaks_exactly_they_get_notified(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(11.0, "room0")
        res, _ = conn_1.handle_input(12.0, "+hello")
        self.assertEqual(2, len(res))
        a = [conn_1.conn_id, conn_2.conn_id]
        b = [res[0][0], res[1][0]]
        a.sort()
        b.sort()
        self.assertEqual(a, b)

    def test_a_comes_b_comes_a_goes_one_msg(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(11.0, "room0")
        conn_1.disconnect(12.0, None)
        res, _ = conn_2.handle_input(13.0, "+hello")
        self.assertEqual(1, len(res))
        self.assertEqual(conn_2.conn_id, res[0][0])

    def test_message_in_one_room_is_isolated(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(11.0, "room1")
        res, _ = conn_1.handle_input(12.0, "+1")
        self.assertEqual(1, len(res))
        self.assertEqual(conn_1.conn_id, res[0][0])

    def test_create_room_twice_get_409(self):
        try:
            self.logic.create_room(10.0, "room0")
            self.assertFalse("should have thrown error")
        except Exception as e:
            self.assertEqual(409, e.status_code)

    def test_if_room_doesnt_exist_404(self):
        try:
            self.logic.connect(10.0, "nonexistent")
            self.assertFalse("should have thrown error")
        except Exception as e:
            self.assertEqual(404, e.status_code)

    def test_connect_get_others_last_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res_1, _ = conn_1.handle_input(10.1, "+1")
        res_2, conn_2 = self.logic.connect(10.2, "room0")
        self.assertEqual(1, len(res_2))
        self.assertEqual(res_1[0][1]["last"],
                         res_2[0][1]["last"])

    def test_on_connect_get_up_to_date(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        conn_1.handle_input(10.1, "+old")
        res_1, _ = conn_1.handle_input(99.0, "+new")
        res_2, conn_2 = self.logic.connect(99.1, "room0")
        self.assertEqual(res_1[0][1], res_1[0][1])

    def test_connect_get_no_moments(self):
        res, conn_1 = self.logic.connect(10.0, "room0")
        self.assertEqual(1, res[0][1]["n"])

    def test_speaking_right_after_joining_merges(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res, _ = conn_1.handle_input(10.4, "+1")
        self.assertEqual(1, res[0][1]["n"])

    def test_speaking_after_joining_creates_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res, _ = conn_1.handle_input(10.6, "+1")
        self.assertEqual(2, res[0][1]["n"])

    def test_interrupting_creates_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(10.7, "+1")
        res, _ = conn_2.handle_input(11.3, "+2")
        self.assertEqual(3, res[0][1]["n"])

    def test_interrupting_quickly_doesnt_count(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(10.7, "+1")
        res, _ = conn_2.handle_input(11.1, "+2")
        self.assertEqual(2, res[0][1]["n"])

    def test_database_starts_empty(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, moments = self.logic.get_moments_range(10.2, ("room0", None, None))
        self.assertEqual({"start": 0, "end": 1, "moments": [[]]},
                         moments)

    def test_interrupt_and_fetch_moments_get_socket_moments(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        before, _ = conn_1.handle_input(10.2, "+1")
        after, _ = conn_2.handle_input(10.8, "+2")
        _, m = self.logic.get_moments_range(10.9, ("room0", 0, 2))
        self.assertEqual(before[0][1]["last"], m[1])
        self.assertEqual(1, len(after[0][1]["last"]))


if __name__ == "__main__":
    unittest.main()
