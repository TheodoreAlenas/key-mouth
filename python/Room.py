from OutputWithDb import OutputWithDb
from PageSplitter import PageSplitter


class Room:

    def __init__(self, splitter_data, room_id, db_room,
                 moments_per_page, next_moment_idx=0, name=None):
        self.splitter_data = splitter_data
        self.room_id = room_id
        self.db = db_room
        self.name = name
        self.output_accumulator = OutputWithDb(db_room, "in " + room_id)
        self.page_splitter = PageSplitter(
            moments_per_page=moments_per_page,
            next_moment_idx=next_moment_idx
        )
        self.conns = []

    def rename(self, name):
        self.db.rename(name)
        self.name = name
