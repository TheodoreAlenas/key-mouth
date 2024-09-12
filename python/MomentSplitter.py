from dataclasses import dataclass


@dataclass
class ConfTiming:
    min_silence: float
    min_moment: float


@dataclass
class MomentSplitterData:
    last_moment_time: float


class MomentSplitter:

    def __init__(self, conf_timing, room):
        self._conf_timing = conf_timing
        self.last_spoke = 0.0
        self.room = room

    def get_should_split(self, time):
        started_speaking = (time - self.last_spoke >
                            self._conf_timing.min_silence)
        moment_lasted = (time - self.room.last_moment_time >
                         self._conf_timing.min_moment)
        self.last_spoke = time
        if started_speaking and moment_lasted:
            self.room.last_moment_time = time
            return True
        return False
