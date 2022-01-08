from django.contrib.auth.models import User
from testing.testcases import TestCase
from datetime import timedelta
from utils.time_helpers import utc_now

class TweetTests(TestCase):

    def setUp(self):
        self.yimin = self.create_user('yimin')
        self.tweet = self.create_tweet(self.yimin, content='Niubi, Niubi, Niubi')

    def test_hours_to_now(self):
        self.tweet.created_at = utc_now() - timedelta(hours=10)
        self.tweet.save()
        self.assertEqual(self.tweet.hours_to_now(), 10)

    def test_like_set(self):
        self.create_like(self.yimin, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)
        # duplicate like
        self.create_like(self.yimin, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)
        theshy = self.create_user('theshy')
        self.create_like(theshy, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 2)
