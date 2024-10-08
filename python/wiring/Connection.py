
# License at the bottom

from lib.exceptions import LogicHttpException


class Connection:

    def __init__(self, conn_id, room, moment_splitter):
        self.conn_id = conn_id
        self.room = room
        self.moment_splitter = moment_splitter

    def connect(self, time, _):
        self.room.conns.append(self.conn_id)
        last_few = self.room.pers_out_map.get_last_pages(n=1)
        conn_msg = self._handle_parsed(time, "connect")
        return ([(self.conn_id, last_few)] + conn_msg, self)

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

        if self.moment_splitter.get_should_split(time):
            if self.room.page_splitter.get_should_split():
                self.room.pers_out_map.save_last_page()
                nmi = self.room.page_splitter.next_moment_idx
                to_bcast += self._push(0, 'newPage', nmi)
            to_bcast += self._push(0, 'newMoment', time)

        to_bcast += self._push(self.conn_id, inp_type, body)
        return to_bcast

    def _push(self, conn_id, event_type, body):
        v = self.room.pers_out_map.push(conn_id, event_type, body)
        return [(conn, v) for conn in self.room.conns]


class Broadcaster(Connection):

    def close_room(self, time):
        self._handle_parsed(time, "shutdown")

    def say_created(self, time):
        self._push(0, 'newPage', 0)
        self._push(0, 'newMoment', time)
        self._handle_parsed(time, "create")

    def say_started(self, time):
        self._handle_parsed(time, "start")


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
