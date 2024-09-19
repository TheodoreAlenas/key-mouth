from dataclasses import dataclass


class DbMapper:

    def push_event(self, event):
        if event.event_type == 'newPage':
            self.last_page = {
                'firstMomentIdx': event.body,
                'moments': []
            }
        elif event.event_type == 'newMoment':
            self.get_last_page()['moments'].append({
                'time': event.body,
                'diffs': []
            })
        else:
            self.last_page['moments'][-1]['diffs'].append({
                'connId': event.conn_id,
                'type': event.event_type,
                'body': event.body
            })

    def get_last_page(self):
        return self.last_page


@dataclass
class ViewEvent:
    conn_id: any
    event_type: str
    body: any


def db_model_to_events(pages):

    events = []

    for page in pages:
        events.append(ViewEvent(
            conn_id=0,
            event_type='newPage',
            body=page['firstMomentIdx']
        ))
        for m in page['moments']:
            events.append(ViewEvent(
                conn_id=0,
                event_type='newMoment',
                body=m['time']
            ))
            for d in m['diffs']:
                events.append(ViewEvent(
                    conn_id=d['connId'],
                    event_type=d['type'],
                    body=d['body']
                ))

    return events

