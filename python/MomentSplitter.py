from dataclasses import dataclass


@dataclass
class ConfTiming:
    min_silence: float
    min_moment: float


class MomentSplitter:

    def __init__(self, conf_timing, room):
        self._conf_timing = conf_timing
        self.last_spoke = 0.0
        self.room = room

    def interrupted_conversation(self, time):
        started_speaking = (time - self.last_spoke >
                            self._conf_timing.min_silence)
        moment_lasted = (time - self.room.last_moment_time >
                         self._conf_timing.min_moment)
        return started_speaking and moment_lasted

    def update_just_spoke(self, time):
        self.last_spoke = time
