from db.event_adapter import db_model_to_events
from OutputWithDb import OutputWithDb, OutputMapper


class Room:

    def __init__(self, room_id, db_room,
                 next_moment_idx, moment_splitter_data, splitter,
                 unsaved_page=None, name=None):
        self.room_id = room_id
        self.db = db_room
        self.name = name
        self.moment_splitter_data = moment_splitter_data
        self.splitter = splitter
        self.output_accumulator = OutputWithDb(
            db=db_room,
            next_moment_idx=next_moment_idx,
            debug_context_str="in " + room_id,
        )
        if unsaved_page is not None:
            for e in db_model_to_events([unsaved_page]):
                self.output_accumulator.push_event(e)
        self.conns = []

    def rename(self, name):
        self.db.rename(name)
        self.name = name

    def get_pages_range(self, start, end):
        to_stream = OutputMapper(start, 0)
        db_model = self.db.get_range(start, end)
        events = db_model_to_events(db_model)
        for e in events:
            to_stream.push(e)
        return to_stream.get_last_page()
