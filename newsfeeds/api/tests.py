from newsfeeds.models import NewsFeed
from friendships.models import Friendship
from rest_framework.test import APIClient
from testing.testcases import TestCase


NEWSFEEDS_URL = '/api/newsfeeds/'
POST_TWEETS_URL = '/api/tweets/'
FOLLOW_URL = '/api/friendships/{}/follow/'


class NewsFeedApiTests(TestCase):

    def setUp(self):
        self.yimin = self.create_user('yimin')
        self.yimin_client = APIClient()
        self.yimin_client.force_authenticate(self.yimin)

        self.theshy = self.create_user('theshy')
        self.theshy_client = APIClient()
        self.theshy_client.force_authenticate(self.theshy)

        # create followings and followers for theshy
        for i in range(2):
            follower = self.create_user('theshy_follower{}'.format(i))
            Friendship.objects.create(from_user=follower, to_user=self.theshy)
        for i in range(3):
            following = self.create_user('theshy_following{}'.format(i))
            Friendship.objects.create(from_user=self.theshy, to_user=following)

    def test_list(self):
        # 需要登录
        response = self.anonymous_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 403)
        # 不能用 post
        response = self.yimin_client.post(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 405)
        # 一开始啥都没有
        response = self.yimin_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['newsfeeds']), 0)
        # 自己发的信息是可以看到的
        self.yimin_client.post(POST_TWEETS_URL, {'content': 'Hello World'})
        response = self.yimin_client.get(NEWSFEEDS_URL)
        self.assertEqual(len(response.data['newsfeeds']), 1)
        # 关注之后可以看到别人发的
        self.yimin_client.post(FOLLOW_URL.format(self.theshy.id))
        response = self.theshy_client.post(POST_TWEETS_URL, {
            'content': 'Hello Ywitter',
        })
        posted_tweet_id = response.data['id']
        response = self.yimin_client.get(NEWSFEEDS_URL)
        self.assertEqual(len(response.data['newsfeeds']), 2)
        self.assertEqual(response.data['newsfeeds'][0]['tweet']['id'], posted_tweet_id)
