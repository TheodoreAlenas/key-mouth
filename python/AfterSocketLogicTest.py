from AfterSocketLogic import AfterSocketLogic, AfterSocketPublicLogic, ConfTiming, RoomExistsException
from DbMock import DbMock
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

    def test_merged_moments_dont_chain_beyond_the_config(self):
        conns = []
        for i in range(7):
            _, conn = self.logic.connect(10.0 + 0.1 * i, "room0")
            conns.append(conn)
        ns = []
        for i in range(7):
            res, _ = conns[i].handle_input(99.0 + 0.1 * i, "+hi")
            ns.append(res[0][1]["n"])
        self.assertEqual(2, ns[4])
        self.assertEqual(3, ns[6])

    def test_database_starts_empty(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, moments = self.logic.get_moments_range(10.2, ("room0", None, None))
        self.assertEqual({"start": 0, "end": 1,
                          "moments": [{'moment': [], 'time': 10.0}]},
                         moments)

    def test_interrupt_and_fetch_moments_get_socket_moments(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        before, _ = conn_1.handle_input(10.2, "+1")
        after, _ = conn_2.handle_input(10.8, "+2")
        _, m = self.logic.get_moments_range(10.9, ("room0", 0, 2))
        self.assertEqual(before[0][1]["last"], m[1]["moment"])
        self.assertEqual(1, len(after[0][1]["last"]))
        self.assertEqual(10.8, m[1]["time"])


class DbLoadRoomTest(unittest.TestCase):

    def get_logic(self, time, db_mock):
        return AfterSocketPublicLogic(AfterSocketLogic(
            time=time,
            db=db_mock,
            conf_timing=ConfTiming(
                min_silence=3.0,
                min_moment=0.5
            )))

    def test_use_other_db_start_blank(self):
        logic_1 = self.get_logic(10.0, DbMock())
        logic_1.create_room(10.1, "room0")
        logic_2 = self.get_logic(10.2, DbMock())
        try:
            logic_2.connect(10.3, "room0")
            self.assertFalse("should have thrown an error")
        except Exception:
            pass

    def test_use_same_db_dont_start_blank(self):
        db = DbMock()
        logic_1 = self.get_logic(10.0, db)
        logic_1.create_room(10.1, "room0")
        logic_2 = self.get_logic(10.2, db)
        logic_2.connect(10.3, "room0")

    def test_use_same_db_see_stored_moment_and_not_last(self):
        db = DbMock()

        logic_1 = self.get_logic(10.0, db)
        logic_1.create_room(10.1, "room0")
        _, conn = logic_1.connect(10.2, "room0")
        conn.handle_input(10.3, "+will be stored later")

        logic_2 = self.get_logic(10.3, db)
        res, _ = logic_2.connect(10.4, "room0")
        self.assertEqual({'last': [], 'n': 1}, res[0][1])
        self.assertEqual(1, len(res))

        conn.handle_input(99.0, "+started speaking again, stored old")
        logic_3 = self.get_logic(99.1, db)
        res, _ = logic_3.connect(99.2, "room0")
        self.assertEqual({'last': [], 'n': 2}, res[0][1])
        self.assertEqual(1, len(res))


class DbLoadLastMomentTimeTest(unittest.TestCase):

    def get_logic(self, time, db_mock):
        return AfterSocketPublicLogic(AfterSocketLogic(
            time=time,
            db=db_mock,
            conf_timing=ConfTiming(
                min_silence=3.0,
                min_moment=0.5
            )))

    def setUp(self):

        self.db = DbMock()

        logic = self.get_logic(10.0, self.db)
        logic.create_room(10.1, "room0")
        _, conn = logic.connect(10.2, "room0")
        conn.handle_input(10.3, "+will be stored later")
        conn.handle_input(99.0, "+started speaking again, stored old")

        logic = self.get_logic(99.1, self.db)
        _, conn = logic.connect(99.2, "room0")
        self.conn = conn

    def test_merge_new_fast(self):
        res, _ = self.conn.handle_input(99.4, "+should merge")
        self.assertEqual(2, res[0][1]['n'])

    def test_dont_merge_new_slow(self):
        res, _ = self.conn.handle_input(99.6, "+shouldn't merge")
        self.assertEqual(3, res[0][1]['n'])


if __name__ == "__main__":
    unittest.main()
