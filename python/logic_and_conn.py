class ConnRoomData:

    def __init__(self, time, name, moments):
        self.name = name
        self.last_moment = []
        self.conns = []
        self.last_moment_time = time
        self.moments = moments


class ConfTiming:

    def __init__(self, min_silence, min_moment):
        self.min_silence = min_silence
        self.min_moment = min_moment
