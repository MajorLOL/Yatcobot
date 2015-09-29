import os
import unittest
import logging
import datetime
from unittest.mock import patch, MagicMock

import requests_mock
from freezegun import freeze_time

from yatcobot.client import TwitterClient, TwitterClientException

logging.disable(logging.ERROR)


class TestTwitterClient(unittest.TestCase):
    """Tests for TwitterClient class"""
    tests_path = path = os.path.dirname(os.path.abspath(__file__))

    ratelimits_full = {'/collections/list': {'limit': 1000, 'reset': 1443529669, 'percent': 100.0, 'remaining': 1000}, '/followers/list': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/contacts/addressbook': {'limit': 300, 'reset': 1443529669, 'percent': 100.0, 'remaining': 300}, '/account/update_profile': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/search/tweets': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/users/lookup': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/saved_searches/destroy/:id': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/users/profile_banner': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/lists/subscribers': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/help/tos': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/trends/place': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/application/rate_limit_status': {'limit': 180, 'reset': 1443529669, 'percent': 99.44444444444444, 'remaining': 179}, '/friends/following/list': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/lists/ownerships': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/account/login_verification_enrollment': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/contacts/users_and_uploaded_by': {'limit': 300, 'reset': 1443529669, 'percent': 100.0, 'remaining': 300}, '/users/derived_info': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/statuses/friends': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/statuses/user_timeline': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/lists/subscriptions': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/saved_searches/show/:id': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/users/show/:id': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/direct_messages/sent': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/help/privacy': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/friendships/incoming': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/statuses/home_timeline': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/statuses/retweeters/ids': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/geo/similar_places': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/lists/statuses': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/geo/id/:place_id': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/statuses/oembed': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/geo/search': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/device/token': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/collections/entries': {'limit': 1000, 'reset': 1443529669, 'percent': 100.0, 'remaining': 1000}, '/friendships/outgoing': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/lists/members': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/followers/ids': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/statuses/retweets/:id': {'limit': 60, 'reset': 1443529669, 'percent': 100.0, 'remaining': 60}, '/contacts/delete/status': {'limit': 300, 'reset': 1443529669, 'percent': 100.0, 'remaining': 300}, '/users/suggestions/:slug': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/friendships/show': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/lists/members/show': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/mutes/users/ids': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/account/settings': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/contacts/users': {'limit': 300, 'reset': 1443529669, 'percent': 100.0, 'remaining': 300}, '/friendships/no_retweets/ids': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/direct_messages': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/lists/subscribers/show': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/statuses/retweets_of_me': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/moments/permissions': {'limit': 300, 'reset': 1443529669, 'percent': 100.0, 'remaining': 300}, '/statuses/lookup': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/blocks/ids': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/statuses/show/:id': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/users/suggestions/:slug/members': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/trends/available': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/mutes/users/list': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/blocks/list': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/users/search': {'limit': 180, 'reset': 1443529669, 'percent': 100.0, 'remaining': 180}, '/geo/reverse_geocode': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/contacts/uploaded_by': {'limit': 300, 'reset': 1443529669, 'percent': 100.0, 'remaining': 300}, '/statuses/mentions_timeline': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/friends/following/ids': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/help/settings': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/direct_messages/show': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/lists/memberships': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/help/configuration': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/favorites/list': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/direct_messages/sent_and_received': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/users/report_spam': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/friends/ids': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/friendships/lookup': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/account/verify_credentials': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/friends/list': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/lists/list': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/collections/show': {'limit': 1000, 'reset': 1443529669, 'percent': 100.0, 'remaining': 1000}, '/help/languages': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/saved_searches/list': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/lists/show': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/users/suggestions': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}, '/trends/closest': {'limit': 15, 'reset': 1443529669, 'percent': 100.0, 'remaining': 15}}
    ratelimits_empty = {'/geo/search': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/saved_searches/destroy/:id': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/statuses/friends': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/device/token': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/friends/ids': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/statuses/home_timeline': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/users/suggestions': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/contacts/delete/status': {'reset': 100, 'percent': 0, 'limit': 300, 'remaining': 0}, '/friendships/outgoing': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/users/suggestions/:slug/members': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/friends/list': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/account/login_verification_enrollment': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/geo/similar_places': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/ownerships': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/subscriptions': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/blocks/ids': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/direct_messages/sent_and_received': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/contacts/addressbook': {'reset': 100, 'percent': 0, 'limit': 300, 'remaining': 0}, '/users/show/:id': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/contacts/users': {'reset': 100, 'percent': 0, 'limit': 300, 'remaining': 0}, '/account/settings': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/trends/closest': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/members': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/users/report_spam': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/followers/ids': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/account/verify_credentials': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/saved_searches/list': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/statuses/retweeters/ids': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/direct_messages/sent': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/users/profile_banner': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/favorites/list': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/mutes/users/list': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/statuses/oembed': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/users/derived_info': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/list': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/help/languages': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/mutes/users/ids': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/statuses/lookup': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/help/settings': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/show': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/trends/available': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/subscribers': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/friendships/no_retweets/ids': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/friends/following/list': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/trends/place': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/geo/id/:place_id': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/contacts/uploaded_by': {'reset': 100, 'percent': 0, 'limit': 300, 'remaining': 0}, '/lists/members/show': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/friendships/lookup': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/search/tweets': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/collections/entries': {'reset': 100, 'percent': 0, 'limit': 1000, 'remaining': 0}, '/friendships/show': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/application/rate_limit_status': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/statuses/show/:id': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/friends/following/ids': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/users/search': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/contacts/users_and_uploaded_by': {'reset': 100, 'percent': 0, 'limit': 300, 'remaining': 0}, '/statuses/retweets_of_me': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/geo/reverse_geocode': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/statuses/mentions_timeline': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/memberships': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/help/privacy': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/statuses/user_timeline': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/help/configuration': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/subscribers/show': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/collections/show': {'reset': 100, 'percent': 0, 'limit': 1000, 'remaining': 0}, '/moments/permissions': {'reset': 100, 'percent': 0, 'limit': 300, 'remaining': 0}, '/account/update_profile': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/blocks/list': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/direct_messages': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/users/lookup': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/users/suggestions/:slug': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/lists/statuses': {'reset': 100, 'percent': 0, 'limit': 180, 'remaining': 0}, '/help/tos': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/direct_messages/show': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/statuses/retweets/:id': {'reset': 100, 'percent': 0, 'limit': 60, 'remaining': 0}, '/saved_searches/show/:id': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/collections/list': {'reset': 100, 'percent': 0, 'limit': 1000, 'remaining': 0}, '/friendships/incoming': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}, '/followers/list': {'reset': 100, 'percent': 0, 'limit': 15, 'remaining': 0}}


    def setUp(self):
        self.client = TwitterClient('Consumer Key', "Consumer Secret", "Access Key", "Access Secret")
        self.client.ratelimits = self.ratelimits_full

    @requests_mock.mock()
    def test_search_tweets(self, m):
        with open(self.tests_path + '/fixtures/search_tweets.json') as f:
            response = f.read()
        m.get('https://api.twitter.com/1.1/search/tweets.json?q=210462857140252672&result_type=mixed&count=50',
                                                                                                    text=response)
        r = self.client.search_tweets("210462857140252672", 50)
        self.assertEqual(len(r), 4)

    @requests_mock.mock()
    def test_retweet(self, m):
        with open(self.tests_path + '/fixtures/statuses_retweet.json') as f:
            response = f.read()
        m.post('https://api.twitter.com/1.1/statuses/retweet/241259202004267009.json', text=response)
        r = self.client.retweet("241259202004267009")
        self.assertEqual(r['retweeted_status']['id'], 241259202004267009)

    @requests_mock.mock()
    def test_get_tweet(self, m):
        with open(self.tests_path + '/fixtures/statuses_show.json') as f:
            response = f.read()
        m.get('https://api.twitter.com/1.1/statuses/show/210462857140252672.json', text=response)
        r = self.client.get_tweet("210462857140252672")
        self.assertEqual(r['id'], 210462857140252672)

    @requests_mock.mock()
    def test_get_friends_ids(self, m):
        with open(self.tests_path + '/fixtures/friends_ids.json') as f:
            response = f.read()
        m.get('https://api.twitter.com/1.1/friends/ids.json', text=response)
        r = self.client.get_friends_ids()
        self.assertEqual(len(r), 31)

    @requests_mock.mock()
    def test_follow(self, m):
        with open(self.tests_path + '/fixtures/friendship_create.json') as f:
            response = f.read()
        m.post('https://api.twitter.com/1.1/friendships/create.json', text=response)
        r = self.client.follow(1401881)
        self.assertEqual(r['id'], 1401881)

    @requests_mock.mock()
    def test_unfollow(self, m):
        with open(self.tests_path + '/fixtures/friendship_create.json') as f:
            response = f.read()
        m.post('https://api.twitter.com/1.1/friendships/destroy.json', text=response)
        r = self.client.unfollow(1401881)
        self.assertEqual(r['id'], 1401881)

    @requests_mock.mock()
    def test_favorite(self, m):
        with open(self.tests_path + '/fixtures/favorites_create.json') as f:
            response = f.read()
        m.post('https://api.twitter.com/1.1/favorites/create.json', text=response)
        r = self.client.favorite(243138128959913986)
        self.assertEqual(r['id'], 243138128959913986)

    @requests_mock.mock()
    def test_get_blocks(self, m):
        with open(self.tests_path + '/fixtures/blocks_ids.json') as f:
            response = f.read()
        m.get('https://api.twitter.com/1.1/blocks/ids.json', text=response)
        r = self.client.get_blocks()
        self.assertEqual(len(r), 1)

    @requests_mock.mock()
    def test_update_ratelimits(self, m):
        #revert original function
        with open(self.tests_path + '/fixtures/application_rate_limit_status.json') as f:
            response = f.read()

        m.get('https://api.twitter.com/1.1/application/rate_limit_status.json', text=response)
        self.client.update_ratelimits(False)
        self.assertEqual(len(self.client.ratelimits), 80)
        #check if percent is computed
        for x in self.client.ratelimits.values():
            self.assertIn('percent', x)
            self.assertEqual(x['limit'] / 100 * x['percent'], x['remaining'])

    @requests_mock.mock()
    def test_api_call_error(self, m):
        with open(self.tests_path + '/fixtures/error.json') as f:
            response = f.read()
        m.get(requests_mock.ANY, text=response)
        with self.assertRaises(TwitterClientException):
            self.client._api_call('blocks/ids')

    def test_check_ratelimit_with_no_more_remaining(self):
        self.client.ratelimits = self.ratelimits_empty

        self.client.update_ratelimits = MagicMock()

        with freeze_time(datetime.datetime.fromtimestamp(0)):
            for key in self.ratelimits_empty.keys():
                with patch('time.sleep') as p:
                    self.client._check_ratelimit(key)
                    p.assert_called_with(100)



