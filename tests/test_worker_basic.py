
import unittest
import codecs
import os

from mothership.base import MothershipServer
from workers.basic_worker import BasicUserParseWorker

class TestWorkerBasic(unittest.TestCase):

    def test_basic_worker_connection(self):
        """
        Purpose: Test regular running of worker
        Expectation: startup system, hit the reddit user and parse the data, fail to send to mothership (exception)

        :precondition: Mothership server not running
        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(Exception, worker.run)

    def test_worker_parsing(self):
        """
        Purpose: Test regular parsing mechanisms of worker
        Expectation: Load html file, send it to worker to parse, should return list of results

        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        file_path = '%s/%s' % (os.path.dirname(os.path.realpath(__file__)), 'test_resources/sample_GET_response.html')

        with codecs.open(file_path, encoding='utf-8') as f:
            text = f.read().encode('ascii', 'ignore')

        results, next_page = worker.parse_text(str(text).strip().replace('\r\n', ''))

        self.assertGreater(len(results), 0)     # Check that results are returned
        self.assertEqual(len(results[0]), 3)    # Check that results are in triplets (check formatting)

    def test_worker_add_links_max_limit(self):
        worker = None
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        worker.max_links = 0
        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links("test.com")
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before)
        
    def test_worker_add_links_to_crawled_1(self):
        """
        Purpose: Test if cur_links is added correctly
        Expectation: added one urls by calling the add_links funcition, the add_links increased to 2

        :return:
        """
        worker = None 
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        worker.to_crawl = ["https://www.reddit.com/user/Chrikelnel"]
        worker.add_links(["https://www.google.ca/"])
        
        self.assertRaises(Exception, worker.run)

        self.assertEqual(worker.cur_links, 2)


    def test_worker_add_links_to_crawled_2(self):
        """
        Purpose: Test if cur_links will be added if the duplicated link is added accidently
        Expectation: added two urls, the add_links increased to 2, not 3 (filtered out when append to the to_crawl list)

        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        worker.to_crawl = ["https://www.reddit.com/user/Chrikelnel"]
        worker.add_links(["https://www.google.ca/"])
        worker.add_links(["https://www.google.ca/"])
        self.assertRaises(Exception, worker.run)
        self.assertEqual(worker.cur_links, 2)


    def test_basic_connection_with_mothership_listen(self):
        """
        Purpose: Test regular listen function of server
        Expectation: startup system, hit the reddit user and parse the data, send to mothership and success.

        :precondition: Mothership server running
        :return:
        """
        mothership = MothershipServer()
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(Exception, worker.run)




