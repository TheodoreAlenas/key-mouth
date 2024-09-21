
class OutputMapper:

    def __init__(self, first_moment_idx, first_diff_idx=0):
        self.mi = first_moment_idx
        self.di = first_diff_idx
        self.last_page = []

    def update_page_ended(self):
        self.last_page = []

    def get_last_page(self):
        return self.last_page

    def push(self, event):
        m = {
            'momentIdx': self.mi,
            'diffIdx': self.di,
            'connId': event.conn_id,
            'type': event.event_type,
            'body': event.body
        }
        self.last_page.append(m)
        if event.event_type == 'newMoment':
            self.di = 0
            self.mi += 1
        else:
            self.di += 1
        return m
