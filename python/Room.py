from db.event_adapter import db_model_to_events
from OutputWithDb import OutputWithDb


class PageSplitter:

    def __init__(self, moments_per_page, next_moment_idx):
        self.moments_per_page = moments_per_page
        self.next_moment_idx = next_moment_idx

    def get_should_split(self):
        self.next_moment_idx += 1
        return self.next_moment_idx % self.moments_per_page == 0

    def get_next_moment_idx(self):
        return self.next_moment_idx


class Room:

    def __init__(self, splitter_data, room_id, db_room,
                 moments_per_page, next_moment_idx=0,
                 unsaved_page=None, name=None):
        self.splitter_data = splitter_data
        self.room_id = room_id
        self.db = db_room
        self.name = name
        self.output_accumulator = OutputWithDb(
            db=db_room,
            next_moment_idx=next_moment_idx,
            debug_context_str="in " + room_id,
        )
        self.page_splitter = PageSplitter(
            moments_per_page=moments_per_page,
            next_moment_idx=next_moment_idx,
        )
        if unsaved_page is not None:
            for _ in unsaved_page:  # one day, this will screw me over
                self.page_splitter.get_should_split()
            for e in db_model_to_events([unsaved_page]):
                self.output_accumulator.push_event(e)
        self.nobody_talked_yet = True
        self.conns = []

    def rename(self, name):
        self.db.rename(name)
        self.name = name
