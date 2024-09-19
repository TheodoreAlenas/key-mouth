from dataclasses import dataclass


@dataclass
class RoomData:
    moments_n: int = 0


@dataclass
class Res:
    should_split_page: bool
    should_say_new_page: bool


class PageSplitter:

    def __init__(self, moments_per_page, room: RoomData):
        self.moments_per_page = moments_per_page
        self.room = room

    def update(self) -> Res:
        self.room.moments_n += 1
        should_split = self.room.moments_n % self.moments_per_page == 0
        return PageSplitterRes(
            should_split, should_split or self.room.moments_n == 0)
