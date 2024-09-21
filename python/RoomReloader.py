
# License at the bottom

from Room import Room
from MomentSplitter import MomentSplitterData
from Splitter import Splitter
from dataclasses import dataclass


@dataclass
class Data:
    moments_per_page: int
    db: any


class RoomReloader(Data):

    def load(self):
        rooms_ram = {}
        saved = self.db.get_reloadable_state()
        unsaved_pages = {}
        if saved is not None:
            unsaved_pages = saved.unsaved_pages
        restart_data = self.db.get_restart_data()
        for d in restart_data:
            unsaved_page = unsaved_pages[d.room_id]
            moment_splitter_data = MomentSplitterData(
                last_moment_time=unsaved_page['moments'][-1]['time'],
            )
            next_moment_idx = d.pages_n * self.moments_per_page
            unsaved_moments = len(unsaved_page['moments'])
            splitter=Splitter(
                moments_per_page=self.moments_per_page,
                next_moment_idx=next_moment_idx + 1 + unsaved_moments,
            )
            r = Room(
                room_id=d.room_id,
                name=d.name,
                db_room=self.db.get_room(d.room_id),
                unsaved_page=unsaved_page,
                next_moment_idx=next_moment_idx,
                moment_splitter_data=moment_splitter_data,
                splitter=splitter,
            )
            rooms_ram[d.room_id] = r
        return (rooms_ram, saved)

    def create(self, room_id):
        return Room(
            room_id=room_id,
            db_room=self.db.get_room(room_id),
            next_moment_idx=0,
            moment_splitter_data=MomentSplitterData(
                last_moment_time=None,
            ),
            splitter=Splitter(
                moments_per_page=self.moments_per_page,
                next_moment_idx=0,
            )
        )

    def close(self, time, last_id, rooms):
        unsaved_pages = {}
        for room in rooms:
            room.conn_bcaster.close_room(time)
            unsaved_pages[room.room_id] = \
                room.output_accumulator.get_unsaved_page()
        self.db.set_reloadable_state(
            last_id=last_id,
            unsaved_pages=unsaved_pages
        )


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
