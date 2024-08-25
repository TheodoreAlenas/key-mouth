
class EventStreamAdapter:

    def __init__(self, first_moment_idx, first_diff_idx):
        self.mi = first_moment_idx
        self.di = first_diff_idx
        self.stream_models = []

    def push(self, event):
        m = {
            'momentIdx': self.mi,
            'diffIdx': self.di,
            'connId': event.conn_id,
            'type': event.event_type,
            'body': event.body
        }
        self.stream_models.append(m)
        if event.event_type == 'endOfMoment':
            self.di = 0
            self.mi += 1
        else:
            self.di += 1
        return m
