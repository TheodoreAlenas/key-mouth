from MomentSplitter import MomentSplitter, MomentSplitterData


class Splitter:

    def __init__(self, moments_per_page, next_moment_idx):
        self.moments_per_page = moments_per_page
        self.next_moment_idx = next_moment_idx
        self.nobody_talked_yet = True

    def split(self, should_split_moment, first_arg,
              say_new_page, say_new_moment, save_last_page):

        if self.nobody_talked_yet:
            self.nobody_talked_yet = False
            if self.next_moment_idx == 0:
                say_new_page(first_arg, next_moment_idx=0)
            say_new_moment(first_arg)

        if should_split_moment:
            self.next_moment_idx += 1
            if self.next_moment_idx % self.moments_per_page == 0:
                save_last_page(first_arg)
                say_new_page(
                    first_arg,
                    next_moment_idx=self.next_moment_idx
                )
            say_new_moment(first_arg)

    def split_with_nop_callbacks(self, should_split_moment):
        def nop(_, next_mome):
            pass
        self.split(
            should_split_moment=should_split_moment,
            first_arg=None,
            say_new_page=nop,
            say_new_moment=nop,
            save_last_page=nop,
        )
