class IntTestWidgets:

    def __init__(self):
        self.raised_exceptions = []

    def raise_exception_once(self, msg):
        if not msg in self.raised_exceptions:
            self.raised_exceptions.append(msg)
            raise Exception("for inttest: " + msg)
