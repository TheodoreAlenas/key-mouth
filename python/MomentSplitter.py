from dataclasses import dataclass


@dataclass
class ConfTiming:
    min_silence: float
    min_moment: float


@dataclass
class MomentSplitterData:
    last_moment_time: float


@dataclass
class MomentSplitterRes:
    should_split: bool
    nobody_had_talked: bool


class MomentSplitter:

    def __init__(self, conf_timing, room):
        self._conf_timing = conf_timing
        self.last_spoke = 0.0
        self.room = room
        self.nobody_talked_yet = True

    def update(self, time):
        nobody_had_talked = self._update_nobody_talked()
        should_split = self._get_should_split(time)
        self._update_timers(time, should_split)
        return MomentSplitterRes(should_split, nobody_had_talked)

    def _update_nobody_talked(self):
        nobody_had_talked = self.nobody_talked_yet
        self.nobody_talked_yet = False
        return nobody_had_talked

    def _get_should_split(self, time):
        started_speaking = (time - self.last_spoke >
                            self._conf_timing.min_silence)
        moment_lasted = (time - self.room.last_moment_time >
                         self._conf_timing.min_moment)
        return started_speaking and moment_lasted

    def _update_timers(self, time, should_split):
        self.last_spoke = time
        if should_split:
            self.room.last_moment_time = time
