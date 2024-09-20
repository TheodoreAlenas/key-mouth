from Splitter import Splitter
import unittest


class SplitterA(unittest.TestCase):

    def setUp(self):
        self.s = Splitter(moments_per_page=2, next_moment_idx=0)
        self.l = []

    def split_with(self, should_split_moment):
        def say_new_page(l, next_moment_idx):
            l.append(f'say_new_page next_moment_idx={next_moment_idx}')
        def say_new_moment(l):
            l.append('say_new_moment')
        def save_last_page(l):
            l.append('save_last_page')
        self.s.split(
            should_split_moment=should_split_moment,
            first_arg=self.l,
            say_new_page=say_new_page,
            say_new_moment=say_new_moment,
            save_last_page=save_last_page,
        )

    def test_first_time_speaking_new_everything(self):
        self.split_with(False)
        self.assertEqual([
            'say_new_page next_moment_idx=0',
            'say_new_moment',
        ], self.l)

    def test_no_moment_split_twice_no_difference(self):
        self.split_with(False)
        self.split_with(False)
        self.assertEqual([
            'say_new_page next_moment_idx=0',
            'say_new_moment',
        ], self.l)

    def test_no_moment_split_yes_moment_split(self):
        self.split_with(False)
        self.split_with(True)
        self.assertEqual([
            'say_new_page next_moment_idx=0',
            'say_new_moment',
            'say_new_moment',
        ], self.l)

    def test_2_splits_per_page_limit(self):
        self.split_with(False)
        self.split_with(True)
        self.split_with(True)
        self.assertEqual([
            'say_new_page next_moment_idx=0',
            'say_new_moment',
            'say_new_moment',
            'save_last_page',
            'say_new_page next_moment_idx=2',
            'say_new_moment',
        ], self.l)

    def test_yes_moment_split(self):
        def f():
            self.split_with(True)
        self.assertRaises(Exception, f)

    def test_start_with_almost_full_page(self):
        self.s = Splitter(moments_per_page=10, next_moment_idx=9)
        self.split_with(False)
        self.assertEqual([
            'say_new_moment',
        ], self.l)
        self.split_with(True)
        self.assertEqual([
            'say_new_moment',
            'save_last_page',
            'say_new_page next_moment_idx=10',
            'say_new_moment',
        ], self.l)

    def test_start_with_10_full_pages_and_one_almost_full(self):
        self.s = Splitter(moments_per_page=10, next_moment_idx=99)
        self.split_with(False)
        self.split_with(True)
        self.assertEqual([
            'say_new_moment',
            'save_last_page',
            'say_new_page next_moment_idx=100',
            'say_new_moment',
        ], self.l)

    def test_works_same_as_last_time(self):
        self.split_with(False)
        self.split_with(True)
        self.split_with(True)
        self.split_with(True)
        self.split_with(False)
        self.split_with(True)
        self.split_with(False)
        self.split_with(False)
        self.split_with(False)
        self.split_with(True)
        self.split_with(False)
        self.split_with(True)
        self.split_with(True)
        self.assertEqual([
            'say_new_page next_moment_idx=0',
            'say_new_moment',
            'say_new_moment',
            'save_last_page',
            'say_new_page next_moment_idx=2',
            'say_new_moment',
            'say_new_moment',
            'save_last_page',
            'say_new_page next_moment_idx=4',
            'say_new_moment',
            'say_new_moment',
            'save_last_page',
            'say_new_page next_moment_idx=6',
            'say_new_moment',
            'say_new_moment',
        ], self.l)


class SplitterB(unittest.TestCase):

    def setUp(self):
        self.l = []
        self.s = Splitter(moments_per_page=2, next_moment_idx=0)
        self.split_with(False)
        self.split_with(True)
        self.split_with(True)
        self.split_with(True)
        self.original = self.l
        self.l = []

    def split_with(self, should_split_moment):
        def say_new_page(l, next_moment_idx):
            l.append(f'say_new_page next_moment_idx={next_moment_idx}')
        def say_new_moment(l):
            l.append('say_new_moment')
        def save_last_page(l):
            l.append('save_last_page')
        self.s.split(
            should_split_moment=should_split_moment,
            first_arg=self.l,
            say_new_page=say_new_page,
            say_new_moment=say_new_moment,
            save_last_page=save_last_page,
        )

    def test_restart_at_new_page(self):

        self.s = Splitter(moments_per_page=2, next_moment_idx=0)
        self.split_with(False)
        self.split_with(True)
        l1 = self.l
        self.l = []

        self.s = Splitter(moments_per_page=2, next_moment_idx=2)
        self.split_with(False)
        self.split_with(True)
        l2 = self.l
        self.l = []

        self.assertEqual(self.original, l1 + l2)

    def test_restart_before_new_page(self):

        self.s = Splitter(moments_per_page=2, next_moment_idx=0)
        self.split_with(False)
        l1 = self.l
        self.l = []

        self.s = Splitter(moments_per_page=2, next_moment_idx=1)
        self.split_with(False)
        self.split_with(True)
        self.split_with(True)
        l2 = self.l
        self.l = []

        self.assertEqual(self.original, l1 + l2)


if __name__ == '__main__':
    unittest.main()
