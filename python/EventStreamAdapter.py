
class EventStreamAdapter:

    def __init__(self, first_moment_idx, first_diff_idx):
        self.mi = first_moment_idx
        self.di = first_diff_idx

    def to_db_model(self, event):
        t = event.event_type
        ans = {
            'momentIdx': self.mi,
            'diffIdx': self.di,
            'connId': event.conn_id,
            'type': t,
            'body': event.body
        }
        if t == 'endOfMoment':
            self.di = 0
            self.mi += 1
        else:
            self.di += 1
        return ans
