from AfterSocketLogic import AfterSocketLogic, Moments
import unittest


class AfterSocketLogicTest(unittest.TestCase):

    def setUp(self):
        self.logic = AfterSocketLogic(Moments())

    def tearDown(self):
        self.logic.cleanup()

    def test_one_conn_one_msg(self):
        _, conn_id = self.logic.register(10.0)
        res = self.logic.handle_input(11.0, conn_id, "+")
        self.assertEqual([], res)
        res = self.logic.handle_input(12.0, conn_id, "hello")
        self.assertEqual(
            [(
                conn_id,
                [{"connId": conn_id, "type": "write", "body": "hello"}]
            )],
            res)

    def test_two_conn_one_msg_bcast(self):
        _, conn_1 = self.logic.register(10.0)
        _, conn_2 = self.logic.register(11.0)
        self.logic.handle_input(12.0, conn_1, "+")
        res = self.logic.handle_input(13.0, conn_1, "hello")
        self.assertEqual(2, len(res))
        self.assertEqual(res[0][1], res[1][1])
        a = [conn_1, conn_2]
        b = [res[0][0], res[1][0]]
        a.sort()
        b.sort()
        self.assertEqual(a, b)

    def test_a_comes_b_comes_a_goes_one_msg(self):
        _, conn_1 = self.logic.register(10.0)
        _, conn_2 = self.logic.register(11.0)
        self.logic.disconnect(12.0, conn_1)
        self.logic.handle_input(12.0, conn_1, "+")
        res = self.logic.handle_input(13.0, conn_2, "hello")
        self.assertEqual(
            [(
                conn_2,
                [{"connId": conn_2, "type": "write", "body": "hello"}]
            )],
            res)

    def test_two_conn_one_msg_each_and_last_goes_last(self):
        _, conn_1 = self.logic.register(10.0)
        _, conn_2 = self.logic.register(11.0)
        self.logic.handle_input(      11.0, conn_1, "+")
        self.logic.handle_input(      12.0, conn_2, "+")
        self.logic.handle_input(      13.0, conn_2, "2")
        res = self.logic.handle_input(14.0, conn_1, "1")
        self.assertEqual([
            {"connId": conn_2, "type": "write", "body": "2"},
            {"connId": conn_1, "type": "write", "body": "1"}
        ], res[0][1])
        self.assertEqual(res[0][1], res[1][1])


if __name__ == "__main__":
    unittest.main()
