from db.event_adapter import EventDbAdapter
from EventStreamAdapter import EventStreamAdapter
from dataclasses import dataclass


class ConnRoomData:

    def __init__(self, last_moment_time, room_id, db_room, name=None):
        self.last_moment_time = last_moment_time
        self.room_id = room_id
        self.db = db_room
        self.name = name
        self.evt_db = EventDbAdapter()
        self.evt_stream = EventStreamAdapter(self.db.get_len(), 0)
        self.conns = []

    def rename(self, name):
        self.db.rename(name)
        self.name = name


@dataclass
class ConfTiming:
    min_silence: float
    min_moment: float
