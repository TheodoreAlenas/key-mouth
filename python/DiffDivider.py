class DiffDivider:

    next_user_id = 0
    moments = {}
    recent_ungrouped = []

    def __init__(self,
                 time_start,
                 max_merge,
                 min_silence,
                 min_speech):

        self.latest_update = self.time_start = time_start
        self.max_merge = max_merge
        self.min_silence = min_silence
        self.min_speech = min_speech

    def register(self):
        i = self.next_user_id
        self.next_user_id += 1
        return i

    def size(self):
        return len(self.moments)

    def new_diff(self, conn_id, diff):
        self.moments[len(self.moments)] = [{
            "connId": conn_id,
            "time": self.latest_update,
            "diff": diff
        }]

    def get(self, i):
        return self.moments[i]

    def get_recent_ungrouped(self):
        return self.recent_ungrouped

    def update(self, time):
        if time - self.latest_update > self.min_silence:
            self.moments[len(self.moments)] = self.recent_ungrouped
            self.recent_ungrouped = []
        self.latest_update = time

