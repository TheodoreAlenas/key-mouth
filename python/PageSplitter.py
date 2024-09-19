from dataclasses import dataclass


@dataclass
class Res:
    should_split: bool
    should_say_new: bool
    next_moment_idx: int | None


class PageSplitter:

    def __init__(self, moments_per_page, next_moment_idx):
        self.moments_per_page = moments_per_page
        self.next_moment_idx = next_moment_idx

    def update(self) -> Res:
        self.next_moment_idx += 1
        should_split = self.next_moment_idx % self.moments_per_page == 0
        return PageSplitterRes(
            should_split=should_split,
            should_say_next=should_split or self.next_moment_idx == 0,
            next_moment_idx=self.next_moment_idx
        )
