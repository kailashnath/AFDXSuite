import unittest

class SampleTest(unittest.TestCase):

    def setUp(self):
        print 'setup'

    def testSample(self):
        print 'testing sample'
        self.failUnless('a' == 'b', "Failed message")

    def testAnother(self):
        print 'testing another'

if __name__ == '__main__':
    unittest.main()
