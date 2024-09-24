
class OutputMapper:

    def __init__(self, first_moment_idx, first_diff_idx=0):
        self.mi = first_moment_idx
        self.di = first_diff_idx
        self.buf = []

    def clear(self):
        self.buf = []

    def get(self):
        return self.buf

    def push(self, event):
        if event.event_type == 'newPage':
            self.di = 0
        m = {
            'momentIdx': self.mi,
            'diffIdx': self.di,
            'connId': event.conn_id,
            'type': event.event_type,
            'body': event.body
        }
        self.buf.append(m)
        if event.event_type == 'newMoment':
            self.di = 0
            self.mi += 1
        else:
            self.di += 1
        return m
