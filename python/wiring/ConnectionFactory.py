from wiring.Connection import Connection, Broadcaster
from lib.MomentSplitter import MomentSplitter


class ConnectionFactory:

    def __init__(self, min_silence, min_moment, last_id):
        self.min_silence = min_silence
        self.min_moment = min_moment
        self.last_id = last_id or 100

    def connection(self, room):
        self.last_id += 1
        return Connection(
            conn_id=self.last_id,
            room=room,
            moment_splitter=MomentSplitter(
                min_silence=self.min_silence,
                min_moment=self.min_moment,
                room=room.moment_splitter_data,
            )
        )

    def broadcaster(self, room):
        return Broadcaster(
            conn_id=0,
            room=room,
            moment_splitter=MomentSplitter(
                min_silence=self.min_silence,
                min_moment=self.min_moment,
                room=room.moment_splitter_data,
            )
        )
