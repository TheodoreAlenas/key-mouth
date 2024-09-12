from OutputWithDb import OutputWithDb


class ConnRoomData:

    def __init__(self, splitter_data, room_id, db_room, name=None):
        self.splitter_data = splitter_data
        self.room_id = room_id
        self.db = db_room
        self.name = name
        self.output_accumulator = OutputWithDb(db_room, "in " + room_id)
        self.conns = []

    def rename(self, name):
        self.db.rename(name)
        self.name = name
