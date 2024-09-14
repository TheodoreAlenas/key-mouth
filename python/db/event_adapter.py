from dataclasses import dataclass


class DbMapper:

    def push(self, event):
        if event.event_type == 'newMoment':
            self.m = {'time': event.body, 'diffs': []}
        else:
            self.m['diffs'].append({
                'connId': event.conn_id,
                'type': event.event_type,
                'body': event.body
            })

    def get_moment(self):
        return self.m


@dataclass
class ViewEvent:
    conn_id: any
    event_type: str
    body: any


def db_model_to_events(moments):

    events = []

    for m in moments:
        events.append(ViewEvent(
            conn_id=0,
            event_type='newMoment',
            body=m['time']))
        for d in m['diffs']:
            events.append(ViewEvent(
                conn_id=d['connId'],
                event_type=d['type'],
                body=d['body']))

    return events

