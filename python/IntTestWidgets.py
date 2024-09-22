from time import time


class IntTestWidgets:

    def __init__(self):
        self.raised_exceptions = []

    def raise_exception_once(self, msg):
        if not msg in self.raised_exceptions:
            self.raised_exceptions.append(msg)
            raise Exception("for inttest: " + msg)

    def add_room_and_restart(self, logic, create_logic):
        logic.create_room(time(), 'pre\nmade')
        logic.close(time(), None)
        return create_logic(
            min_silence=0.2,
            min_moment=0.2
        )
