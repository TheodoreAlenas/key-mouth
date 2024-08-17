
# License at the bottom

from logic_and_conn import ConnRoomData, ConfTiming


class Conn:

    def __init__(self, conn_id, room: ConnRoomData, conf_timing: ConfTiming):
        self.conn_id = conn_id
        self.room = room
        self._conf_timing = conf_timing
        self.last_spoke = 0.0

    def connect(self, time, _):
        self.room.conns.append(self.conn_id)
        res, _ = self._handle_parsed(time, "connect")
        return (res, self)

    def disconnect(self, time, _):
        self.room.conns.remove(self.conn_id)
        return self._handle_parsed(time, "disconnect")

    def handle_input(self, time, data):
        if len(data) < 2:
            return ([], None)
        if data[0] == '+':
            return self._handle_parsed(time, "write", data[1:])
        elif data[0] == '-':
            return self._handle_parsed(time, "delete", data[1:])
        return ([], None)

    def _handle_parsed(self, time, inp_type, body=None):
        if self._interrupted_conversation(time):
            self._bake_moment_to_be_stored(time)
        self._append_and_update(time, inp_type, body)
        return self._get_last_moment_broadcast_list()

    def _interrupted_conversation(self, time):
        started_speaking = (time - self.last_spoke >
                            self._conf_timing.min_silence)
        moment_lasted = (time - self.room.last_moment_time >
                         self._conf_timing.min_moment)
        return started_speaking and moment_lasted

    def _bake_moment_to_be_stored(self, time):
        baked_moment = self.room.last_moment
        self.room.moments.add_moment(time, baked_moment)
        self.room.last_moment = []
        self.room.last_moment_time = time

    def _append_and_update(self, time, inp_type, body):
        self.last_spoke = time
        self.room.last_moment.append({
            "connId": self.conn_id,
            "type": inp_type,
            "body": body
        })

    def _get_last_moment_broadcast_list(self):
        s = {"n": self.room.moments.get_len(),
                "last": self.room.last_moment}
        return ([(conn, s) for conn in self.room.conns], None)

    def _a(self):
        return {"n": self.room.moments.get_len(),
                "last": self.room.last_moment}

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
