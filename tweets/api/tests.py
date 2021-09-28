from rest_framework.test import APIClient
from testing.testcases import TestCase
from tweets.models import Tweet

'''
List all API QUERY URL HERE, REMEMBER ADD '/' AT THE END, OR IT WILL LEAD TO REDIRECT 301
'''
TWEET_LIST_API = '/api/tweets/'  # get
TWEET_CREATE_API = '/api/tweets/' # post

class TweetApiTests(TestCase):

    def setUp(self):
        self.yimin = self.create_user('yimin', 'yimin@AGenius.com')
        self.tweets1 = [
            self.create_tweet(self.yimin) for i in range(3) # yimin create three tweets
        ]
        self.yimin_client = APIClient()
        self.yimin_client.force_authenticate(self.yimin)

        self.theshy = self.create_user('theshy', 'theshy@Agenius.com')
        self.tweets2 = [
            self.create_tweet(self.theshy) for i in range(2) # theshy create two tweets
        ]

    def test_list_api(self):
        ## QUERY WITH USER ID
        response = self.anonymous_client.get(TWEET_LIST_API)
        self.assertEqual(response.status_code, 400)

        ## COMMON REQUEST
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.yimin.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 3)
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.theshy.id})
        self.assertEqual(len(response.data['tweets']), 2)
        ## TEST THE ORDER
        self.assertEqual(response.data['tweets'][0]['id'], self.tweets2[1].id)
        self.assertEqual(response.data['tweets'][1]['id'], self.tweets2[0].id)


    def test_create_api(self):
        # WITH LOGIN
        response = self.anonymous_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 403)
        # WITH CONTENT
        response = self.yimin_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 400)
        # CONTENT SHOULD NOT BE TOO SHORT
        response = self.yimin_client.post(TWEET_CREATE_API, {'content':'1'})
        self.assertEqual(response.status_code, 400)
        # CONTENT SHOULD NOT BE TOO LONG
        response = self.yimin_client.post(TWEET_CREATE_API, {
            'content': '0' * 141
        })
        self.assertEqual(response.status_code, 400)

        # SHARE TWEETS
        tweets_count = Tweet.objects.count()
        response = self.yimin_client.post(TWEET_CREATE_API, {
            'content': 'Hello yimin, this is my first tweet!'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.yimin.id)
        self.assertEqual(Tweet.objects.count(), tweets_count + 1)