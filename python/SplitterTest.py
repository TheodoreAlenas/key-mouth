from Splitter import Splitter
import unittest


class SplitterA(unittest.TestCase):

    def test_3_per_page_zebra(self):
        s = Splitter(
            moments_per_page=3,
            next_moment_idx=0,
        )
        a = [s.get_should_split() for _ in range(6)]
        self.assertEqual([False, False, True, False, False, True], a)

    def test_starting_from_arbitrary_point(self):
        a = [
            Splitter(
                moments_per_page=3,
                next_moment_idx=i
            ).get_should_split()
            for i in range(6)
        ]
        self.assertEqual([False, False, True, False, False, True], a)


if __name__ == "__main__":
    unittest.main()
