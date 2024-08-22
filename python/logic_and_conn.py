from db.event_adapter import EventDbAdapter
from EventStreamAdapter import EventStreamAdapter


class ConnRoomData:

    def __init__(self, last_moment_time, room_id, db_room, name=None):
        self.room_id = room_id
        self.name = name
        self.db = db_room
        self.evt_db = EventDbAdapter()
        self.evt_stream = EventStreamAdapter(self.db.get_len(), 0)
        self.conns = []
        self.last_moment_time = last_moment_time

    def rename(self, name):
        self.db.rename(name)
        self.name = name


class ConfTiming:

    def __init__(self, min_silence, min_moment):
        self.min_silence = min_silence
        self.min_moment = min_moment
