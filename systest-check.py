import unittest


class BackCheck(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BackCheck, self).__init__(*args, **kwargs)
        with open("git-ignores/systest-logs-back") as f:
            self.lines = f.readlines()

    def one_says(self, text):
        for i in range(self.cur, len(self.lines)):
            if self.lines[i].find(text):
                return True
        return False

    def setUp(self):
        self.cur = 0

    def test_requested_socket_and_last_messages(self):
        self.assertTrue(self.one_says(' - "GET /last HTTP/1.1" 200'))
        self.cur = 0
        self.assertTrue(self.one_says(' - "WebSocket /" [accepted]'))

    def test_connection_open_and_closed(self):
        self.assertTrue(self.one_says(' - connection open'))
        self.assertTrue(self.one_says(' - connection closed'))

    def test_gracefuly_shut_down(self):
        self.assertTrue(self.lines[-3].find(" - Waiting for application shutdown.") != -1)
        self.assertTrue(self.lines[-2].find(" - Application shutdown complete.") != -1)
        self.assertTrue(self.lines[-1].find(" - Finished server process ") != -1)


class FrontCheck(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(FrontCheck, self).__init__(*args, **kwargs)
        with open("git-ignores/systest-logs-front") as f:
            self.lines = f.readlines()

    def one_says(self, text):
        for i in range(self.cur, len(self.lines)):
            if self.lines[i].find(text):
                return True
        return False

    def setUp(self):
        self.cur = 0

    def test_first_set_old_moments(self):
        self.assertTrue(self.lines[0].find("old moments set to") != -1)

    def test_input_set_in_right_order(self):
        self.assertTrue(self.lines[1].endswith("input value set to 'hi'\n"))
        self.assertTrue(self.lines[2].endswith("input value set to ' there'\n"))
        self.assertTrue(self.lines[3].endswith("input value set to ''\n"))

    def test_no_excess_events(self):
        self.assertTrue(len(self.lines) == 4)


if __name__ == "__main__":
    unittest.main()
