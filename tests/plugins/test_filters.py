import unittest

from tests.helper_func import load_fixture_config, create_post
from yatcobot.config import TwitterConfig
from yatcobot.plugins.filters import FilterABC, FilterMinRetweets
from yatcobot.post_queue import PostQueue


class TestFilterABC(unittest.TestCase):

    def setUp(self):
        load_fixture_config()

    def test_get_enabled(self):
        for method in TwitterConfig.get().search.filter.values():
            method['enabled'] = True
        self.assertEqual(len(FilterABC.get_enabled()), len(TwitterConfig.get().search.filter))

        for method in TwitterConfig.get().search.filter.values():
            method['enabled'] = False
        self.assertEqual(len(FilterABC.get_enabled()), 0)


class TestFilterMinRetweets(unittest.TestCase):

    def setUp(self):
        load_fixture_config()
        self.method = FilterMinRetweets()

    def test_filter_by_min_retweets(self):
        TwitterConfig.get()['search']['filter']['min_retweets']['enabled'] = True
        TwitterConfig.get()['search']['filter']['min_retweets']['number'] = 10

        posts = {
            1: create_post(id=1, retweets=1),
            2: create_post(id=2, retweets=5),
            3: create_post(id=3, retweets=15),
            4: create_post(id=4, retweets=20),
        }

        queue = PostQueue(posts)

        self.method.filter(queue)

        self.assertEqual(len(queue), 2)

        for post_id, post in queue.items():
            self.assertGreaterEqual(post['retweet_count'], 10)

    def test_enabled(self):
        TwitterConfig.get()['search']['filter']['min_retweets']['enabled'] = True
        self.assertTrue(self.method.is_enabled())

        TwitterConfig.get()['search']['filter']['min_retweets']['enabled'] = False
        self.assertFalse(self.method.is_enabled())