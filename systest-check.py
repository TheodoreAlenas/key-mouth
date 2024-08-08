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


class FrontCheck(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(FrontCheck, self).__init__(*args, **kwargs)
        with open("git-ignores/systest-logs-front") as f:
            self.lines = f.readlines()

    def test_input_value_is_set_at_least_once(self):
        a = False
        for l in self.lines:
            if l.find("\tinput value set to '") != -1:
                a = True
        self.assertTrue(a)

    def test_broadcaster_heard_the_same_as_listener(self):
        bcaster_heard = []
        listener_heard = []
        say_last = "\t[say]\tlast moment set to ["
        hear_last = "\t[hear]\tlast moment set to ["
        for l in self.lines:
            pos = l.find(say_last)
            if pos != -1:
                bcaster_heard.append(l[pos + len(say_last):])                
        for l in self.lines:
            pos = l.find(hear_last)
            if pos != -1:
                listener_heard.append(l[pos + len(hear_last):])
        self.assertEqual(bcaster_heard, listener_heard)
        self.assertEqual(4, len(bcaster_heard))

    def test_after_interrupt_old_moments_filled(self):
        stop_last = "<stop last wasn't set>"
        stop_old = "<stop old wasn't set>"
        all_old = "<all old wasn't set>"
        stop_last_str = '\t[stop]\tlast moment set to '
        stop_old_str = '\t[stop]\told moments set to '
        all_old_str = '\t[all]\told moments set to '
        for l in self.lines:
            pos = l.find(stop_last_str)
            if pos != -1:
                stop_last = l[pos + len(stop_last_str):-1]
                break
        for l in self.lines:
            pos = l.find(stop_old_str)
            if pos != -1:
                stop_old = l[pos + len(stop_old_str):]
        for l in self.lines:
            pos = l.find(all_old_str)
            if pos != -1:
                all_old = l[pos + len(all_old_str):]
        self.assertEqual(stop_old, all_old)
        self.assertTrue(all_old.find(stop_last) != -1)

    def test_after_interrupt_last_moment_updates(self):
        stop_last = "<it wasn't set actually>"
        all_last = "<they weren't set actually>"
        stop_last_set_to = '\t[stop]\tlast moment set to '
        all_last_set_to = '\t[all]\tlast moment set to '
        for l in self.lines:
            pos = l.find(stop_last_set_to)
            if pos != -1:
                stop_last = l[pos + len(stop_last_set_to):]
        for l in self.lines:
            pos = l.find(all_last_set_to)
            if pos != -1:
                all_last = l[pos + len(all_last_set_to):]
        self.assertEqual(stop_last, all_last)

    def test_and_the_messages_havent_changed(self):
        m1 = '\t[stop]\tlast moment set to [{"name":"Sotiris0","message":[{"type":"write","body":"hi thereclear"}]}]'
        m2 = '\t[stop]\tlast moment set to [{"name":"Sotiris2","message":[{"type":"write","body":"interrupt"}]}]'
        n1 = n2 = 0
        for l in self.lines:
            if l.find(m1) != -1:
                n1 += 1
            if l.find(m2) != -1:
                n2 += 1
        self.assertEqual((1, 1), (n1, n2))

    def test_unless_interrupt_old_moments_are_nothing(self):
        say = '[say]\told moments set to [[]]'
        hear = '[hear]\told moments set to [[]]'
        stop = '[stop]\told moments set to [[]]'
        n = {"say": 0, "hear": 0, "stop": 0}
        for l in self.lines:
            if l.find(say) != -1:
                n["say"] += 1
            if l.find(hear) != -1:
                n["hear"] += 1
            if l.find(stop) != -1:
                n["stop"] += 1
        self.assertEqual({"say": 1, "hear": 1, "stop": 1}, n)

    def test_as_many_logs_as_last_test_run(self):
        self.assertEqual(20, len(self.lines))


if __name__ == "__main__":
    unittest.main()
