from AfterSocketLogic import AfterSocketLogic, RoomExistsException
from MomentSplitter import ConfTiming
from db.mock import Db
import unittest
from OutputWithDbTest import A
from MomentSplitterTest import MSA


class AParsing(unittest.TestCase):

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

    def test_0_one_conn_one_msg(self):
        res, conn = self.logic.connect(10.0, "room0")
        self.assertEqual(
            [
                (conn.conn_id, {
                    "momentIdx": 0,
                    "diffIdx": 0,
                    "connId": 0,
                    "type": "newMoment",
                    "body": 10.0
                }),
                (conn.conn_id, {
                    "momentIdx": 1,
                    "diffIdx": 0,
                    "connId": 0,
                    "type": "create",
                    "body": None
                }),
                (conn.conn_id, {
                    "momentIdx": 1,
                    "diffIdx": 1,
                    "connId": conn.conn_id,
                    "type": "connect",
                    "body": None
                }),
            ],
            res)
        res, _ = conn.handle_input(10.1, "+hello")
        self.assertEqual(
            [(conn.conn_id, {
                "momentIdx": 1,
                "diffIdx": 2,
                "connId": conn.conn_id,
                "type": "write",
                "body": "hello"
            })],
            res)

    def test_deletion_parsed(self):
        _, conn = self.logic.connect(10.0, "room0")
        res, _ = conn.handle_input(10.1, "-a")
        self.assertEqual('delete', res[0][1]['type'])
        self.assertEqual('a', res[0][1]['body'])


class Broadcasting(unittest.TestCase):

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
        _, self.conn_1 = self.logic.connect(10.0, "room0")
        _, self.conn_2 = self.logic.connect(11.0, "room0")
        _, self.conn_3 = self.logic.connect(11.0, "room1")

    def test_two_conn_one_speaks_they_hear_the_same(self):
        res, _ = self.conn_1.handle_input(12.0, "+hello")
        self.assertEqual(res[0][1], res[1][1])

    def test_two_conn_one_speaks_exactly_they_get_notified(self):
        res, _ = self.conn_1.handle_input(12.0, "+hello")
        self.assertEqual(2, len(res))
        a = [self.conn_1.conn_id, self.conn_2.conn_id]
        b = [res[0][0], res[1][0]]
        a.sort()
        b.sort()
        self.assertEqual(a, b)

    def test_a_comes_b_comes_a_goes_one_msg(self):
        self.conn_1.disconnect(12.0, None)
        res, _ = self.conn_2.handle_input(13.0, "+hello")
        self.assertEqual(1, len(res))
        self.assertEqual(self.conn_2.conn_id, res[0][0])

    def test_message_in_one_room_is_isolated(self):
        res, _ = self.conn_3.handle_input(12.0, "+1")
        self.assertEqual(1, len(res))
        self.assertEqual(self.conn_3.conn_id, res[0][0])


class Rooms(unittest.TestCase):

    def setUp(self):
        self.logic = AfterSocketLogic(
            time=8.0,
            db=Db(),
            conf_timing=ConfTiming(
                min_silence=3.0,
                min_moment=0.5
            ))
        self.logic.create_room(10.0, "room0")

    def test_created_room_listed(self):
        _, ans = self.logic.get_rooms(10.1, None)
        self.assertEqual([{'id': 'room0', 'name': None}], ans)

    def test_deleted_room_not_listed(self):
        self.logic.delete_room(10.0, "room0")
        _, ans = self.logic.get_rooms(10.1, None)
        self.assertEqual([], ans)

    def test_renamed_room_listed_renamed(self):
        self.logic.rename_room(10.0, ("room0", "a name"))
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


class ConnectionIds(unittest.TestCase):

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
        _, self.conn_1 = self.logic.connect(10.0, "room0")
        _, self.conn_2 = self.logic.connect(10.1, "room0")

    def test_connection_ids_start_at_101(self):
        self.assertEqual(101, self.conn_1.conn_id)

    def test_connection_ids_increment(self):
        self.assertEqual(102, self.conn_2.conn_id)

    def test_connection_ids_dont_go_per_room(self):
        self.assertEqual(102, self.conn_2.conn_id)


class Moments(unittest.TestCase):

    def setUp(self):
        self.logic = AfterSocketLogic(
            time=8.0,
            db=Db(),
            conf_timing=ConfTiming(
                min_silence=3.0,
                min_moment=0.5
            ))
        self.logic.create_room(10.0, "room0")

    def test_connect_get_others_last_moment(self):
        res_1, conn_1 = self.logic.connect(10.0, "room0")
        res_2, _ = conn_1.handle_input(10.1, "+1")
        res_3, conn_2 = self.logic.connect(10.2, "room0")
        a = [x for _, x in res_1 + res_2]
        b = [x for _, x in res_3[:-2]]
        self.assertEqual(a, b)

    def test_on_connect_get_a_stored_moment(self):
        res_1, conn_1 = self.logic.connect(10.0, "room0")
        res_2, _ = conn_1.handle_input(10.1, "+old")
        res_3, conn_2 = self.logic.connect(99.0, "room0")
        a = [x for _, x in res_1 + res_2]
        b = [x for _, x in res_3[:len(a)]]
        self.assertEqual(a, b)

    def test_on_connect_get_a_stored_moment_and_new(self):
        res_1, conn_1 = self.logic.connect(10.0, "room0")
        res_2, _ = conn_1.handle_input(10.1, "+old")
        res_3, _ = conn_1.handle_input(99.0, "+new")
        res_4, conn_2 = self.logic.connect(99.1, "room0")
        a = [x for _, x in res_1 + res_2]
        b = [x for _, x in res_4[:len(a)]]
        self.assertEqual(a, b)
        c = [x for _, x in res_3]
        d = [x for _, x in res_4[len(a):len(a) + len(c)]]
        self.assertEqual(c, d)

    def test_connect_get_no_moments(self):
        res, conn_1 = self.logic.connect(10.0, "room0")
        self.assertEqual(1, res[-1][1]['momentIdx'])

    def test_connecting_and_speaking_is_one_stream(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res, _ = conn_1.handle_input(12.9, "+1")
        self.assertEqual(1, res[-1][1]['momentIdx'])

    def test_connecting_pausing_speaking_creates_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        res, _ = conn_1.handle_input(13.1, "+1")
        self.assertEqual(2, res[-1][1]["momentIdx"])

    def test_interrupting_creates_moment(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(100.0, "+1")
        res, _ = conn_2.handle_input(100.6, "+2")
        self.assertEqual(3, res[-1][1]["momentIdx"])

    def test_interrupting_quickly_doesnt_count(self):
        _, conn_1 = self.logic.connect(10.0, "room0")
        _, conn_2 = self.logic.connect(10.1, "room0")
        conn_1.handle_input(100.0, "+1")
        res, _ = conn_2.handle_input(100.4, "+2")
        self.assertEqual(2, res[-1][1]["momentIdx"])

    def test_merged_moments_dont_chain_beyond_the_config(self):
        conns = []
        for i in range(7):
            _, conn = self.logic.connect(10.0 + 0.1 * i, "room0")
            conns.append(conn)
        ns = []
        for i in range(7):
            res, _ = conns[i].handle_input(99.0 + 0.1 * i, "+hi")
            ns.append(res[-1][1]["momentIdx"])
        self.assertEqual(3, ns[4])
        self.assertEqual(4, ns[6])


class DbBasics(unittest.TestCase):

    def setUp(self):
        self.logic = AfterSocketLogic(
            time=8.0,
            db=Db(),
            conf_timing=ConfTiming(
                min_silence=3.0,
                min_moment=0.5
            ))
        self.logic.create_room(10.0, "room0")

    def test_database_starts_empty(self):
        self.logic.connect(10.0, "room0")
        _, moments = self.logic.get_moments_range(10.2, ("room0", 0, 100))
        self.assertEqual([], moments)

    def test_interrupt_and_fetch_moment_get_socket_moment(self):
        res_1, _ = self.logic.connect(10.0, "room0")
        self.logic.connect(100.1, "room0")
        _, m = self.logic.get_moments_range(100.7, ("room0", 0, 2))
        msg_to_1 = [x for _, x in res_1]
        self.assertEqual(msg_to_1, m)

    def test_interrupt_and_fetch_moments_get_socket_moments(self):
        res_1, conn_1 = self.logic.connect(10.0, "room0")
        res_2, conn_2 = self.logic.connect(10.1, "room0")
        res_3, _ = conn_1.handle_input(100.0, "+1")
        res_4, _ = conn_2.handle_input(100.6, "+2")
        _, m3 = self.logic.get_moments_range(100.7, ("room0", 0, 3))
        _, m4 = self.logic.get_moments_range(100.7, ("room0", 0, 4))
        self.assertEqual(m3, m4)
        res_all = res_1 + res_2 + res_3
        msg_to_1 = [x for c, x in res_all if c == conn_1.conn_id]
        msg_to_2 = [x for c, x in res_all if c == conn_2.conn_id]
        self.assertEqual(msg_to_1, msg_to_2)
        self.assertEqual(msg_to_1, m3)


class DbLoadRoom(unittest.TestCase):

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
        logic_1.close(10.2, None)
        logic_2 = self.get_logic(10.3, Db())
        try:
            logic_2.connect(10.4, "room0")
            self.assertFalse("should have thrown an error")
        except Exception:
            pass

    def test_use_same_db_see_shutdown_event(self):
        db = Db()
        logic_1 = self.get_logic(10.0, db)
        logic_1.create_room(10.1, "room0")
        logic_1.close(10.2, None)
        logic_2 = self.get_logic(10.3, db)
        res, _ = logic_2.connect(10.4, "room0")
        self.assertEqual('shutdown', res[-4][1]['type'])
        self.assertEqual('newMoment', res[-3][1]['type'])
        self.assertEqual('start', res[-2][1]['type'])
        self.assertEqual('connect', res[-1][1]['type'])

    def test_shutdown_twice_no_missing_broadcaster_error(self):
        db = Db()
        logic = self.get_logic(10.0, db)
        logic.create_room(10.1, "room0")
        logic.close(10.2, None)
        logic = self.get_logic(10.3, db)
        logic.close(10.4, None)
        logic = self.get_logic(10.5, db)
        logic.close(10.6, None)

    def test_use_same_db_see_last_moment(self):
        db = Db()

        logic = self.get_logic(10.0, db)
        logic.create_room(10.01, "room0")
        _, conn = logic.connect(10.02, "room0")
        conn.handle_input(10.03, "+will be stored later")
        logic.close(10.04, None)

        logic = self.get_logic(10.05, db)
        res, _ = logic.connect(10.06, "room0")

        self.assertEqual(   2   , res[-1][1]['momentIdx'])

    def test_use_same_db_see_stored_moment_and_last(self):
        db = Db()

        logic = self.get_logic(10.0, db)
        logic.create_room(10.1, "room0")
        _, conn = logic.connect(10.2, "room0")
        conn.handle_input(10.3, "+will be stored later")

        conn.handle_input(99.0, "+started speaking again, stored old")
        logic.close(99.1, None)

        logic = self.get_logic(99.2, db)
        res, _ = logic.connect(99.3, "room0")

        self.assertEqual(   3   , res[-1][1]['momentIdx'])

    def test_room_names_reload(self):
        db = Db()

        logic = self.get_logic(10.0, db)
        logic.create_room(10.1, "room0")
        logic.rename_room(10.2, ("room0", "a name"))
        logic.close(10.3, None)

        logic = self.get_logic(10.4, db)
        _, ans = logic.get_rooms(10.5, None)
        self.assertEqual([{'id': 'room0', 'name': "a name"}], ans)

    def test_connection_ids_continue(self):
        db = Db()

        logic = self.get_logic(10.0, db)
        logic.create_room(10.1, "room0")
        _, conn_1 = logic.connect(10.2, "room0")
        logic.close(10.3, None)

        logic = self.get_logic(10.4, db)
        _, conn_2 = logic.connect(10.5, "room0")
        self.assertEqual(1, conn_2.conn_id - conn_1.conn_id)


if __name__ == "__main__":
    unittest.main()
