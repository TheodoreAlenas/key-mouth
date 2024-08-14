import unittest


class BackCheck(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BackCheck, self).__init__(*args, **kwargs)
        with open("git-ignores/systest-logs-back") as f:
            self.lines = f.readlines()

    def setUp(self):
        self.cur = 0

    def test_open_connections_closed(self):
        openConnections = 0
        closedConnections = 0
        for l in self.lines:
            if l.find(' - connection open\n') != -1:
                openConnections += 1
            elif l.find(' - connection closed\n') != -1:
                closedConnections += 1
        self.assertEqual(4, openConnections)
        self.assertEqual(openConnections, closedConnections)

    def test_gracefuly_shut_down(self):
        self.assertTrue(self.lines[-3].find(" - Waiting for application shutdown.\n") != -1)
        self.assertTrue(self.lines[-2].find(" - Application shutdown complete.\n") != -1)
        self.assertTrue(self.lines[-1].find(" - Finished server process [") != -1)


if __name__ == "__main__":
    unittest.main()
