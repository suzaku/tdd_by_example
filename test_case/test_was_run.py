class TestCase(object):
    def __init__(self, name):
        self.name = name

    def run(self, result):
        result.testStarted()

        self.setUp()
        try:
            getattr(self, self.name)()
        except:
            result.testFailed()

        self.tearDown()

    def setUp(self):
        pass

    def tearDown(self):
        pass

class TestResult(object):

    def __init__(self):
        self.runCount = 0
        self.errorCount = 0

    def testStarted(self):
        self.runCount += 1

    def testFailed(self):
        self.errorCount += 1

    def summary(self):
        return "%d run, %d failed" % (self.runCount, self.errorCount)


class WasRun(TestCase):

    def setUp(self):
        self.wasRun = False
        self.log = 'setUp'

    def testMethod(self):
        self.wasRun = True
        self.log += ' testMethod'

    def testBrokenMethod(self):
        raise Exception

    def tearDown(self):
        self.log += ' tearDown'


class TestSuite(object):

    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class TestCaseTest(TestCase):

    def testTemplateMethod(self):
        test = WasRun("testMethod")
        result = TestResult()
        test.run(result)
        assert test.log == 'setUp testMethod tearDown'

    def testResult(self):
        test = WasRun("testMethod")
        result = TestResult()
        test.run(result)
        assert "1 run, 0 failed" == result.summary()

    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        result = TestResult()
        test.run(result)
        assert "1 run, 1 failed" == result.summary()

    def testFailedResultFormatting(self):
        result = TestResult()
        result.testStarted()
        result.testFailed()
        assert "1 run, 1 failed" == result.summary()

    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun('testMethod'))
        suite.add(WasRun('testBrokenMethod'))
        result = TestResult()
        suite.run(result)
        assert "2 run, 1 failed" == result.summary()


suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testSuite"))
result = TestResult()
suite.run(result)
print result.summary()
