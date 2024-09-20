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

    def test_yes_moment_split(self):
        self.split_with(True)
        self.assertEqual([
            'say_new_page next_moment_idx=0',
            'say_new_moment',
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


if __name__ == '__main__':
    unittest.main()
