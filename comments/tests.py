from testing.testcases import TestCase
# Create your tests here.

class CommentModelTests(TestCase):

    def setUp(self):
        self.yimin = self.create_user('yimin')
        self.tweet = self.create_tweet(self.yimin)
        self.comment = self.create_comment(self.yimin, self.tweet)

    def test_comment(self):
        self.assertNotEqual(self.comment.__str__(), None)

    def test_like_set(self):
        self.create_like(self.yimin, self.comment)
        self.assertEqual(self.comment.like_set.count(), 1)

        self.create_like(self.yimin, self.comment)
        self.assertEqual(self.comment.like_set.count(), 1)

        theshy = self.create_user('theshy')
        self.create_like(theshy, self.comment)
        self.assertEqual(self.comment.like_set.count(), 2)