class ConnRoomData:

    def __init__(self, last_moment_time, room_id, db_room, name=None):
        self.room_id = room_id
        self.name = name
        self.last_moment = []
        self.conns = []
        self.last_moment_time = last_moment_time
        self.db = db_room

    def rename(self, name):
        self.db.rename(name)
        self.name = name


class ConfTiming:

    def __init__(self, min_silence, min_moment):
        self.min_silence = min_silence
        self.min_moment = min_moment
