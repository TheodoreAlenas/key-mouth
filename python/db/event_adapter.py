from dataclasses import dataclass

@dataclass
class ViewEvent:
    conn_id: any
    event_type: str
    body: any


class EventDbAdapter:

    def __init__(self):
        self.return_on_pop = None
        self._clear_m()

    def _clear_m(self):
        self.m = {'time': None, 'diffs': []}

    def push(self, event):
        t = event.event_type
        if t == 'endOfMoment':
            self.m['time'] = event.body
            self.return_on_pop = self.m
            self._clear_m()
        else:
            self.m['diffs'].append({
                'connId': event.conn_id,
                'type': t,
                'body': event.body
            })

    def pop_moment(self):
        if self.return_on_pop is None:
            raise Exception('popped moment before endOfMoment: ' +
                            str(self.m))
        p = self.return_on_pop
        self.return_on_pop = None
        return p


def db_model_to_events(moments):

    events = []

    for m in moments:
        for d in m['diffs']:
            events.append(ViewEvent(
                conn_id=d['connId'],
                event_type=d['type'],
                body=d['body']))
        events.append(ViewEvent(
            conn_id=0,
            event_type='endOfMoment',
            body=m['time']))

    return events

