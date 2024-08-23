
# License at the bottom

from ConnRoomData import ConnRoomData, ConfTiming
from db.event_adapter import db_model_to_events
from EventStreamAdapter import EventStreamAdapter


class ViewEvent:

    def __init__(self, event_type, conn_id, body):
        self.event_type = event_type
        self.conn_id = conn_id
        self.body = body


class Connection:

    def __init__(self, conn_id, room: ConnRoomData, conf_timing: ConfTiming):
        self.conn_id = conn_id
        self.room = room
        self._conf_timing = conf_timing
        self.last_spoke = 0.0

    def connect(self, time, _):
        self.room.conns.append(self.conn_id)
        l = self.room.db.get_last_few()
        events = db_model_to_events(l['moments'])
        a = EventStreamAdapter(l['start'], 0)
        for e in events:
            a.push(e)
        stream = a.stream_models + self.room.evt_stream.stream_models
        catch_up = [(self.conn_id, e) for e in stream]
        conn_msg = self._handle_parsed(time, "connect")
        return (catch_up + conn_msg, self)

    def close_room(self, time):
        self._handle_parsed(time, "shutdown")
        self._push(0, 'endOfMoment', time)
        self._store_last_moment(time)

    def disconnect(self, time, _):
        self.room.conns.remove(self.conn_id)
        return (self._handle_parsed(time, "disconnect"), None)

    def handle_input(self, time, data):
        if len(data) < 2:
            return ([], None)
        if data[0] == '+':
            return (self._handle_parsed(time, "write", data[1:]), None)
        elif data[0] == '-':
            return (self._handle_parsed(time, "delete", data[1:]), None)
        return ([], None)

    def _handle_parsed(self, time, inp_type, body=None):
        to_bcast = []
        if self._interrupted_conversation(time):
            to_bcast += self._push(0, 'endOfMoment', time)
            self._store_last_moment(time)
        self.last_spoke = time
        to_bcast += self._push(self.conn_id, inp_type, body)
        return to_bcast

    def _interrupted_conversation(self, time):
        started_speaking = (time - self.last_spoke >
                            self._conf_timing.min_silence)
        moment_lasted = (time - self.room.last_moment_time >
                         self._conf_timing.min_moment)
        return started_speaking and moment_lasted

    def _store_last_moment(self, time):
        baked_moment = self.room.evt_db.pop_moment()
        self.room.evt_stream.stream_models = []
        self.room.db.add_moment(baked_moment)
        self.room.last_moment_time = time

    def _push(self, conn_id, event_type, body):
        ve = ViewEvent(
            conn_id=conn_id,
            event_type=event_type,
            body=body
        )
        self.room.evt_db.push(ve)
        v = self.room.evt_stream.push(ve)
        return [(conn, v) for conn in self.room.conns]


"""
Copyright 2024 <dimakopt732@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
