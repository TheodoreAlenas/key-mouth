from AfterSocketLogic import AfterSocketLogic, Moments
import unittest


class AfterSocketLogicTest(unittest.TestCase):

    def setUp(self):
        self.logic = AfterSocketLogic(Moments())

    def test_one_conn_one_msg(self):
        conn_id = self.logic.register(10.0)
        res = self.logic.handle_input(conn_id, "+", 11.0)
        self.assertEqual([], res)
        res = self.logic.handle_input(conn_id, "hello", 11.0)
        self.assertEqual(
            [(
                conn_id,
                [{"connId": conn_id, "type": "write", "body": "hello"}]
            )],
            res)

if __name__ == "__main__":
    unittest.main()
