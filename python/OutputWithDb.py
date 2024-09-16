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

    def store_last_moment(self, time):
        self.evt_stream.stream_models = []
        baked_moment = self.evt_db.get_moment()
        self.db.add_moment(baked_moment)

    def push(self, conn_id, event_type, body):
        ve = ViewEvent(
            conn_id=conn_id,
            event_type=event_type,
            body=body
        )
        self.evt_db.push(ve)
        return self.evt_stream.push(ve)

    def get_last_few(self):
        l = self.db.get_last_few()
        events = db_model_to_events(l['moments'])
        a = OutputMapper(l['start'], 0)
        for e in events:
            a.push(e)
        from_db = a.stream_models
        not_yet_in_db = self.evt_stream.stream_models
        return {
            "firstMomentIdx": l['start'],
            "moments": from_db + not_yet_in_db
        }
