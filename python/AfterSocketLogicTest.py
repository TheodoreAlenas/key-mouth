from AfterSocketLogic import AfterSocketLogic, ConfTiming, RoomExistsException
from db.mock import Db
import unittest


class AfterSocketLogicTest(unittest.TestCase):

    def setUp(self):
        self.logic = AfterSocketLogic(
            time=8.0,
            db=Db(),
            conf_timing=ConfTiming(
                min_silence=3.0,
                min_moment=0.5
            ))
        self.logic.create_room(10.0, "room0")
        self.logic.create_room(10.0, "room1")

    def test_one_conn_one_msg(self):
        _, conn = self.logic.connect(10.0, "room0")
        res, _ = conn.handle_input(10.1, "+hello")
        self.assertEqual(
            [(
                conn.conn_id,
                {"n": 1, "last": [
                    {
                        "connId": conn.conn_id,
                        "type": "connect",
                        "body": None
                    },
                    {
                        "connId": conn.conn_id,
                        "type": "write",
                        "body": "hello"
                    }
                ]}
            )],
            res)

    def test_deletion_parsed(self):
        _, conn = self.logic.connect(10.0, "room0")
        res, _ = conn.handle_input(10.1, "-a")
        self.assertEqual({
            "connId": conn.conn_id,
            "type": "delete",
            "body": "a"
        }, res[0][1]["last"][1])

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

    def test_deleted_room_not_listed(self):
        self.logic.delete_room(10.0, "room0")
        _, ans = self.logic.get_rooms(10.1, None)
        self.assertEqual([{'id': 'room1', 'name': None}], ans)

    def test_renamed_room_listed_renamed(self):
        self.logic.rename_room(10.0, ("room0", "a name"))
        self.logic.delete_room(10.0, "room1")
        _, ans = self.logic.get_rooms(10.1, None)
        self.assertEqual([{'id': 'room0', 'name': "a name"}], ans)

    def test_create_room_twice_get_409(self):
        try:
            self.logic.create_room(10.0, "room0")
            self.assertFalse("should have thrown error")
        except Exception as e:
            self.assertEqual(409, e.status_code)

    def test_if_room_doesnt_exist_connect_404(self):
        try:
            self.logic.connect(10.0, "nonexistent")
            self.assertFalse("should have thrown error")
        except Exception as e:
            self.assertEqual(404, e.status_code)

    def test_if_room_doesnt_exist_get_moments_range_404(self):
        try:
            self.logic.get_moments_range(
                10.0, ("nonexistent", None, None))
            self.assertFalse("should have thrown error")
        except Exception as e:
            self.assertEqual(404, e.status_code)

    def test_connect_get_others_last_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res_1, _ = conn_1.handle_input(10.1, "+1")
        res_2, conn_2 = self.logic.connect(10.2, "room0")
        self.assertEqual(2, len(res_2))
        self.assertEqual(res_1[0][1]["last"],
                         res_2[0][1]["last"])

    def test_on_connect_get_up_to_date(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        conn_1.handle_input(10.1, "+old")
        res_1, _ = conn_1.handle_input(99.0, "+new")
        res_2, conn_2 = self.logic.connect(99.1, "room0")
        self.assertEqual(res_1[0][1], res_2[0][1])

    def test_connect_get_no_moments(self):
        res, conn_1 = self.logic.connect(10.0, "room0")
        self.assertEqual(1, res[0][1]["n"])

    def test_connecting_and_speaking_is_one_stream(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res, _ = conn_1.handle_input(12.9, "+1")
        self.assertEqual(1, res[0][1]["n"])

    def test_connecting_pausing_speaking_creates_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res, _ = conn_1.handle_input(13.1, "+1")
        self.assertEqual(2, res[0][1]["n"])

    def test_interrupting_creates_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(100.0, "+1")
        res, _ = conn_2.handle_input(100.6, "+2")
        self.assertEqual(3, res[0][1]["n"])

    def test_interrupting_quickly_doesnt_count(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(100.0, "+1")
        res, _ = conn_2.handle_input(100.4, "+2")
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
        self.assertEqual(3, ns[4])
        self.assertEqual(4, ns[6])

    def test_database_starts_empty(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, moments = self.logic.get_moments_range(10.2, ("room0", None, None))
        self.assertEqual({"start": 0, "end": 1,
                          "moments": [{'diffs': [], 'time': 10.0}]},
                         moments)

    def test_interrupt_and_fetch_moments_get_socket_moments(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        before, _ = conn_1.handle_input(100.0, "+1")
        conn_2.handle_input(100.6, "+2")
        _, m = self.logic.get_moments_range(100.7, ("room0", 0, 4))
        self.assertEqual(before[0][1]["last"], m[2]["diffs"])
        self.assertEqual(100.6, m[2]["time"])


class DbLoadRoomTest(unittest.TestCase):

    def get_logic(self, time, db_mock):
        return AfterSocketLogic(
            time=time,
            db=db_mock,
            conf_timing=ConfTiming(
                min_silence=3.0,
                min_moment=0.5
            ))

    def test_use_other_db_start_blank(self):
        logic_1 = self.get_logic(10.0, Db())
        logic_1.create_room(10.1, "room0")
        logic_2 = self.get_logic(10.2, Db())
        try:
            logic_2.connect(10.3, "room0")
            self.assertFalse("should have thrown an error")
        except Exception:
            pass

    def test_use_same_db_dont_start_blank(self):
        db = Db()
        logic_1 = self.get_logic(10.0, db)
        logic_1.create_room(10.1, "room0")
        logic_2 = self.get_logic(10.2, db)
        logic_2.connect(10.3, "room0")

    def test_use_same_db_dont_see_last_moment(self):
        db = Db()

        logic = self.get_logic(10.0, db)
        logic.create_room(10.1, "room0")
        _, conn = logic.connect(10.2, "room0")
        conn.handle_input(10.3, "+will be stored later")

        logic = self.get_logic(10.3, db)
        res, _ = logic.connect(10.4, "room0")
        self.assertEqual(1, len(res))
        self.assertEqual(1, len(res[0][1]['last']))
        self.assertEqual('connect', res[0][1]['last'][0]['type'])

        self.assertEqual(   1   , res[0][1]['n'])

    def test_use_same_db_see_stored_moment_and_not_last(self):
        db = Db()

        logic = self.get_logic(10.0, db)
        logic.create_room(10.1, "room0")
        _, conn = logic.connect(10.2, "room0")
        conn.handle_input(10.3, "+will be stored later")

        conn.handle_input(99.0, "+started speaking again, stored old")

        logic = self.get_logic(99.1, db)
        res, _ = logic.connect(99.2, "room0")
        self.assertEqual(1, len(res))
        self.assertEqual(1, len(res[0][1]['last']))
        self.assertEqual('connect', res[0][1]['last'][0]['type'])

        self.assertEqual(   2   , res[0][1]['n'])

    def test_room_names_reload(self):
        db = Db()

        logic = self.get_logic(10.0, db)
        logic.create_room(10.1, "room0")
        logic.rename_room(10.0, ("room0", "a name"))

        logic = self.get_logic(10.0, db)
        _, ans = logic.get_rooms(10.1, None)
        self.assertEqual([{'id': 'room0', 'name': "a name"}], ans)


if __name__ == "__main__":
    unittest.main()
