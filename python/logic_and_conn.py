class ConnRoomData:

    def __init__(self, last_moment_time, room_id, db_room, name=None):
        self.name = room_id
        self.namename = name
        self.last_moment = []
        self.conns = []
        self.last_moment_time = last_moment_time
        self.moments = db_room

    def rename(self, name):
        self.moments.rename(name)
        self.namename = name


class ConfTiming:

    def __init__(self, min_silence, min_moment):
        self.min_silence = min_silence
        self.min_moment = min_moment
