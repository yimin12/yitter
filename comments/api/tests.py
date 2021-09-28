from testing.testcases import TestCase
from rest_framework.test import APIClient
from comments.models import Comment
from django.utils import timezone

COMMENT_URL = '/api/comments/'

class CommentApiTests(TestCase):

    def setUp(self):
        self.yimin = self.create_user('yimin')
        self.yimin_client = APIClient()
        self.yimin_client.force_authenticate(self.yimin)
        self.theshy = self.create_user('shy')
        self.theshy_client = APIClient()
        self.theshy_client.force_authenticate(self.theshy)

        self.tweet = self.create_tweet(self.yimin)

    def test_create(self):
        # comment by random user with no parameters
        response = self.anonymous_client.post(COMMENT_URL)
        self.assertEqual(response.status_code, 403)
        # comment by admin with no parameters
        response = self.yimin_client.post(COMMENT_URL)
        self.assertEqual(response.status_code, 400)
        # comment with only tweet_id
        response = self.yimin_client.post(COMMENT_URL, {'tweet_id': self.tweet.id})
        self.assertEqual(response.status_code, 400)
        # comment with only content
        response = self.yimin_client.post(COMMENT_URL, {'content':'1'})
        self.assertEqual(response.status_code, 400)
        # comment is too long
        response = self.yimin_client.post(COMMENT_URL, {
            'tweet_id': self.tweet.id,
            'content': '1' * 141,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual('content' in response.data['errors'], True)
        # tweet_id and content
        response = self.yimin_client.post(COMMENT_URL, {
            'tweet_id': self.tweet.id,
            'content': '1',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.yimin.id)
        self.assertEqual(response.data['tweet_id'], self.tweet.id)
        self.assertEqual(response.data['content'], '1')

    def test_update(self):
        comment = self.create_comment(self.yimin, self.tweet, 'original')
        another_tweet = self.create_tweet(self.theshy)
        url = '{}{}/'.format(COMMENT_URL, comment.id)
        # anonymous_client can not post comment
        response = self.anonymous_client.put(url, {'content': 'new'})
        self.assertEqual(response.status_code, 403)
        # not owner can not post comment
        response = self.theshy_client.put(url, {'content': 'new'})
        self.assertEqual(response.status_code, 403)
        comment.refresh_from_db()
        self.assertNotEqual(comment.content, 'new')
        # can not update other information except for content
        before_updated_at = comment.updated_at
        before_created_at = comment.created_at
        now = timezone.now()
        response = self.yimin_client.put(url, {
            'content': 'new',
            'user_id': self.yimin.id,
            'tweet_id': another_tweet.id,
            'created_at': now,
        })
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'new')
        self.assertEqual(comment.user, self.yimin)
        self.assertEqual(comment.tweet, self.tweet)
        self.assertEqual(comment.created_at, before_created_at)
        self.assertNotEqual(comment.created_at, now)
        self.assertNotEqual(comment.updated_at, before_updated_at)

    def test_destroy(self):
        comment = self.create_comment(self.yimin, self.tweet)
        url = '{}{}/'.format(COMMENT_URL, comment.id)
        # anonymous_client can not delete a tweet
        response = self.anonymous_client.delete(url)
        self.assertEqual(response.status_code, 403)
        # not owner can not delete comment
        response = self.theshy_client.delete(url)
        self.assertEqual(response.status_code, 403)
        # onwer can delete the tweet
        count = Comment.objects.count()
        response = self.yimin_client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), count - 1)

    def test_list(self):
        # should include tweet_id
        response = self.anonymous_client.get(COMMENT_URL)
        self.assertEqual(response.status_code, 400)
        # can access by carrying the tweet_id
        response = self.anonymous_client.get(COMMENT_URL, {
            'tweet_id': self.tweet.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['comments']), 0)
        # sort comments by time order
        self.create_comment(self.yimin, self.tweet, '1')
        self.create_comment(self.theshy, self.tweet, '2')
        self.create_comment(self.theshy, self.create_tweet(self.theshy), '3')
        response = self.anonymous_client.get(COMMENT_URL, {
            'tweet_id': self.tweet.id,
        })
        self.assertEqual(len(response.data['comments']), 2)
        self.assertEqual(response.data['comments'][0]['content'], '1')
        self.assertEqual(response.data['comments'][1]['content'], '2')
        # provide user_id and tweet_id, we can only use tweet_id to filter
        response = self.anonymous_client.get(COMMENT_URL, {
            'tweet_id': self.tweet.id,
            'user_id': self.yimin.id,
        })
        self.assertEqual(len(response.data['comments']), 2)