from DiffDivider import DiffDivider
import unittest


class DiffDividerTest(unittest.TestCase):

    def setUp(self):
        self.divider = DiffDivider(
            time_start=10.0,
            max_merge=1.0,
            min_silence=2.0,
            min_speech=3.0
        )
        self.conn_id = self.divider.register()

    def tearDown(self):
        self.divider.moments.clear()

    def test_no_diffs_no_moment(self):
        self.assertEqual(0, self.divider.size())
        self.assertEqual([], self.divider.get_recent_ungrouped())

    def test_one_diff_gets_diff_later(self):
        self.divider.update(time=12.1)
        self.divider.new_diff(
            conn_id=self.conn_id,
            diff={"whatever": 732})
        self.assertEqual(1, self.divider.size())
        self.assertEqual([{
            "connId": self.conn_id,
            "time": 12.1,
            "diff": {"whatever": 732}
        }], self.divider.get(0))
        self.assertEqual([], self.divider.get_recent_ungrouped())

    def test_one_diff_isnt_grouped_immediately(self):
        self.divider.update(time=11.9)
        self.divider.new_diff(
            conn_id=self.conn_id,
            diff={"whatever": 732})
        self.assertEqual(0, self.divider.size())
        self.assertEqual([{
            "connId": self.conn_id,
            "time": 11.9,
            "diff": {"whatever": 732}
        }], self.divider.get_recent_ungrouped())


if __name__ == "__main__":
    unittest.main()
