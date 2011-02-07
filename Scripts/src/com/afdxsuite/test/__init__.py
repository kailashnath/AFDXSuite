import unittest

class SampleTest(unittest.TestCase):

    def testSample(self):
        print 'testing sample'
        self.failUnless('a' == 'b', "Failed message")

    def testAnother(self):
        print 'testing another'

class AnotherTest(unittest.TestCase):
    def testAnother(self):
        print 'Another'

if __name__ == '__main__':
    unittest.main()
