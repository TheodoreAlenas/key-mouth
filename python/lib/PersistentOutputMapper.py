from db.event_adapter import \
    DbMapper, db_model_to_events, get_first_moment_idx
from lib.OutputMapper import OutputMapper
from dataclasses import dataclass


@dataclass
class ViewEvent:
    event_type: str
    conn_id: any
    body: any


class PersistentOutputMapper:

    def __init__(self, db, next_moment_idx, unsaved_page,
                 debug_context_str):
        self.db = db
        self.db_mapper = DbMapper()
        self.output_mapper = OutputMapper(next_moment_idx, 0)
        self.debug_context_str = debug_context_str
        if unsaved_page is not None:
            for e in db_model_to_events([unsaved_page]):
                self.push_event(e)

    def save_last_page(self):
        self.output_mapper.clear()
        page = self.db_mapper.get_last_page()
        self.db.push_page(page)

    def push(self, conn_id, event_type, body):
        ve = ViewEvent(
            conn_id=conn_id,
            event_type=event_type,
            body=body
        )
        self.db_mapper.push_event(ve)
        return self.output_mapper.push(ve)

    def push_event(self, event):
        self.db_mapper.push_event(event)
        return self.output_mapper.push(event)

    def get_last_pages(self, n):
        l = self.db.get_last_pages(n=n)
        events = db_model_to_events(l.pages)
        first_moment_idx = get_first_moment_idx(l.pages)
        a = OutputMapper(first_moment_idx=first_moment_idx)
        for e in events:
            a.push(e)
        from_db = a.get()
        not_yet_in_db = self.output_mapper.get()
        return {
            "firstMomentIdx": first_moment_idx,
            "firstPageIdx": l.first_page_idx,
            "events": from_db + not_yet_in_db
        }

    def get_pages_range(self, start, end):
        db_model = self.db.get_range(start, end)
        events = db_model_to_events(db_model)
        first_moment_idx = 0
        if len(events) > 0:
            assert events[0].event_type == 'newPage'
            first_moment_idx = events[0].body
        mapper = OutputMapper(first_moment_idx, 0)
        for e in events:
            mapper.push(e)
        return mapper.get()

    def get_unsaved_page(self):
        return self.db_mapper.get_last_page()
