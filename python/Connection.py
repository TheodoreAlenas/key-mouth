
# License at the bottom

from MomentSplitter import ConfTiming, MomentSplitter
from exceptions import LogicHttpException


class Connection:

    def __init__(self, conn_id, room, conf_timing: ConfTiming):
        self.conn_id = conn_id
        self.room = room
        self.splitter = MomentSplitter(
            conf_timing=conf_timing,
            room=room.moment_splitter_data,
        )

    def connect(self, time, _):
        self.room.conns.append(self.conn_id)
        last_few = self.room.output_accumulator.get_last_pages()
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

        def say_new_page(to_bcast, next_moment_idx):
            to_bcast += self._push(0, 'newPage', next_moment_idx)

        def say_new_moment(to_bcast):
            to_bcast += self._push(0, 'newMoment', time)

        def save_last_page(_):
            self.room.output_accumulator.save_last_page()

        self.room.splitter.split(
            should_split_moment=self.splitter.get_should_split(time),
            first_arg=to_bcast,
            say_new_page=say_new_page,
            say_new_moment=say_new_moment,
            save_last_page=save_last_page,
        )

        to_bcast += self._push(self.conn_id, inp_type, body)
        return to_bcast

    def _push(self, conn_id, event_type, body):
        v = self.room.output_accumulator.push(conn_id, event_type, body)
        return [(conn, v) for conn in self.room.conns]


class Broadcaster(Connection):

    def close_room(self, time):
        self._handle_parsed(time, "shutdown")

    def say_created(self, time):
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
