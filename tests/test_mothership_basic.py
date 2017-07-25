
import unittest
import time

from mothership.base import MothershipServer
from workers.basic_worker import BasicUserParseWorker

class TestMothershipBasic(unittest.TestCase):
	def sleep(mothership):
		time.sleep(2)

    def test_basic_mothership_listen(self):
        """
        Purpose: Test regular running of worker
        Expectation: startup system, hit the reddit user and parse the data, fail to send to mothership (exception)

        :precondition: Mothership server not running
        :return:
        """
        mothership = MothershipServer()
        threading.Thread(target=self.sleep, args=(mothership)).start()
        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(Exception, mothership.run)




