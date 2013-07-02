class TestCase(object):
    def __init__(self, name):
        self.name = name

    def run(self):
        self.setUp()
        getattr(self, self.name)()
        self.tearDown()

    def setUp(self):
        pass

    def tearDown(self):
        pass


class WasRun(TestCase):

    def setUp(self):
        self.wasRun = False
        self.log = 'setUp'

    def testMethod(self):
        self.wasRun = True
        self.log += ' testMethod'

    def tearDown(self):
        self.log += ' tearDown'


class TestCaseTest(TestCase):

    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run()
        assert test.log == 'setUp testMethod tearDown'

TestCaseTest("testTemplateMethod").run()
