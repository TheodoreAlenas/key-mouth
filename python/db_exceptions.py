class RoomExistsException(Exception):
    def __init__(self, msg="room already exists"):
        super().__init__(msg)


class RoomDoesntExistException(Exception):
    def __init__(self, msg="room doesn't exist"):
        super().__init__(msg)
