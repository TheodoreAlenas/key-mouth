from db.event_adapter import EventDbAdapter, db_model_to_events
from EventStreamAdapter import EventStreamAdapter


class ViewEvent:

    def __init__(self, event_type, conn_id, body):
        self.event_type = event_type
        self.conn_id = conn_id
        self.body = body


class OutputWithDb:

    def __init__(self, db):
        self.db = db
        self.evt_db = EventDbAdapter()
        self.evt_stream = EventStreamAdapter(db.get_len(), 0)

    def store_last_moment(self, time):
        self.evt_stream.stream_models = []
        baked_moment = self.evt_db.pop_moment()
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
        a = EventStreamAdapter(l['start'], 0)
        for e in events:
            a.push(e)
        last = self.evt_stream.stream_models
        return a.stream_models + last
