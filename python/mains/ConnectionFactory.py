from mains.Connection import Connection, Broadcaster
from lib.MomentSplitter import MomentSplitter


class ConnectionFactory:

    def __init__(self, conf_timing):
        self.conf_timing = conf_timing

    def connection(self, conn_id, room):
        return Connection(
            conn_id=conn_id,
            room=room,
            moment_splitter=MomentSplitter(
                conf_timing=self.conf_timing,
                room=room.moment_splitter_data,
            )
        )

    def broadcaster(self, room):
        return Broadcaster(
            conn_id=0,
            room=room,
            moment_splitter=MomentSplitter(
                conf_timing=self.conf_timing,
                room=room.moment_splitter_data,
            )
        )
