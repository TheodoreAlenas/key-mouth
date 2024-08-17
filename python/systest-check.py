import unittest


class BackCheck(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BackCheck, self).__init__(*args, **kwargs)
        with open("git-ignores/systest-logs-back") as f:
            self.lines = f.readlines()

    def test_open_connections_closed(self):
        openConnections = 0
        closedConnections = 0
        for l in self.lines:
            if l == 'connection open\n':
                openConnections += 1
            elif l == 'connection closed\n':
                closedConnections += 1
        self.assertEqual(4, openConnections)
        self.assertEqual(openConnections, closedConnections)

    def test_gracefuly_shut_down(self):
        self.assertEqual(
            self.lines[-3], "Waiting for application shutdown.\n")
        self.assertEqual(
            self.lines[-2], "Application shutdown complete.\n")
        self.assertEqual(
            self.lines[-1][:25], "Finished server process [")

if __name__ == "__main__":
    unittest.main()
