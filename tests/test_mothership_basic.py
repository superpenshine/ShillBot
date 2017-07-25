
import unittest

from mothership.base import MothershipServer
from workers.basic_worker import BasicUserParseWorker

class TestMothershipBasic(unittest.TestCase):
    def test_basic_mothership_listen(self):
        """
        Purpose: Test regular running of worker
        Expectation: startup system, hit the reddit user and parse the data, fail to send to mothership (exception)

        :precondition: Mothership server not running
        :return:
        """
        mothership = MothershipServer()

        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(Exception, mothership.run)

    def test_basic_mothership_contact(self):
    	mothership = MothershipServer()
    	mothership.run()
    	worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
    	self.assertRaises(Exception, worker.run)


