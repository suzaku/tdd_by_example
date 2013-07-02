class TestCase(object):
    def __init__(self, name):
        self.name = name

    def run(self):
        self.setUp()
        getattr(self, self.name)()

    def setUp(self):
        pass


class WasRun(TestCase):

    def setUp(self):
        self.wasRun = False
        self.wasSetUp = True

    def testMethod(self):
        self.wasRun = True


class TestCaseTest(TestCase):

    def setUp(self):
        self.test = WasRun("testMethod")

    def testRunning(self):
        self.test.run()
        assert self.test.wasRun

    def testSetUp(self):
        self.test.run()
        assert self.test.wasSetUp

TestCaseTest("testRunning").run()
TestCaseTest("testSetUp").run()
