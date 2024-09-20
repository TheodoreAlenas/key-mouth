from MomentSplitter import MomentSplitter, MomentSplitterData


class Splitter:

    def __init__(self, last_moment_time, conf_timing,
                 moments_per_page, next_moment_idx):
        self.moment_splitter_data = MomentSplitterData(
            last_moment_time=last_moment_time,
        )
        self.moment_splitter = MomentSplitter(
            conf_timing=conf_timing,
            room=self.moment_splitter_data,
        )
        self.moments_per_page = moments_per_page
        self.next_moment_idx = next_moment_idx
        self.nobody_talked_yet = True

    def split(self, say_new_page, say_new_moment, save_last_page):

        if self.nobody_talked_yet:
            self.nobody_talked_yet = False
            if self.next_moment_idx == 0:
                say_new_page(next_moment_idx=0)
            say_new_moment()

        if self.moment_splitter.get_should_split(time):
            self.next_moment_idx += 1
            if self.next_moment_idx % self.moments_per_page == 0:
                save_last_page()
                say_new_page(next_moment_idx=self.next_moment_idx)
            say_new_moment()
