
class Room:

    def __init__(self, room_id, db_room, name,
                 moment_splitter_data, page_splitter, pers_out_map):
        self.room_id = room_id
        self.db = db_room
        self.name = name
        self.moment_splitter_data = moment_splitter_data
        self.page_splitter = page_splitter
        self.pers_out_map = pers_out_map
        self.conns = []

    def rename(self, name):
        self.db.rename(name)
        self.name = name
