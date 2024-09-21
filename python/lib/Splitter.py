
class Splitter:

    def __init__(self, moments_per_page, next_moment_idx):
        self.moments_per_page = moments_per_page
        self.next_moment_idx = next_moment_idx

    def get_should_split(self):
        self.next_moment_idx += 1
        return self.next_moment_idx % self.moments_per_page == 0
