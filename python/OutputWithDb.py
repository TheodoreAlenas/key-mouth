from db.event_adapter import DbMapper, db_model_to_events
from OutputMapper import OutputMapper
from dataclasses import dataclass


@dataclass
class ViewEvent:
    event_type: str
    conn_id: any
    body: any


class OutputWithDb:

    def __init__(self, db, debug_context_str="context unset"):
        self.db = db
        self.evt_db = DbMapper()
        self.evt_stream = OutputMapper(db.get_len(), 0)
        self.debug_context_str = debug_context_str

    def save_last_page(self):
        self.evt_stream.update_page_ended()
        page = self.evt_db.get_last_page()
        self.db.push_page(page)

    def push(self, conn_id, event_type, body):
        ve = ViewEvent(
            conn_id=conn_id,
            event_type=event_type,
            body=body
        )
        self.evt_db.push_event(ve)
        return self.evt_stream.push(ve)

    def get_last_pages(self):
        l = self.db.get_last_pages()
        events = db_model_to_events(l.pages)
        a = OutputMapper(first_moment_idx=l.first_moment_idx)
        for e in events:
            a.push(e)
        from_db = a.get_last_page()
        not_yet_in_db = self.evt_stream.get_last_page()
        return {
            "firstMomentIdx": l.first_moment_idx,
            "events": from_db + not_yet_in_db
        }
