from dataclasses import dataclass


@dataclass
class ConfTiming:
    min_silence: float
    min_moment: float


@dataclass
class MomentSplitterData:
    last_moment_time: float | None = None


class MomentSplitter:

    def __init__(self, conf_timing, room):
        self._conf_timing = conf_timing
        self.last_spoke = None
        self.room = room

    def get_should_split(self, time):
        started_speaking = self._get_started_speaking(time)
        moment_lasted = self._get_moment_lasted(time)
        should_split = started_speaking and moment_lasted
        self._update_timers(time, should_split)
        return should_split

    def _get_started_speaking(self, time):
        if self.last_spoke is None:
            return True
        else:
            return (time - self.last_spoke >=
                    self._conf_timing.min_silence)

    def _get_moment_lasted(self, time):
        if self.room.last_moment_time is None:
            return False
        else:
            return (time - self.room.last_moment_time >=
                    self._conf_timing.min_moment)

    def _update_timers(self, time, should_split):
        self.last_spoke = time
        if should_split or self.room.last_moment_time is None:
            self.room.last_moment_time = time
