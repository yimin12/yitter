from django.test import TestCase as DjangoTestCase
from comments.models import Comment
from django.contrib.auth.models import User
from tweets.models import Tweet
from rest_framework.test import APIClient

# public test initialization
class TestCase(DjangoTestCase):

    @property
    def anonymous_client(self):
        if hasattr(self, '_anonymous_client'):
            return self._anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client

    def create_user(self, username, email=None, password=None):
        if email is None:
            email = '{}@Agenius.com'.format(username)
        if password is None:
            password = 'generic password'
        return User.objects.create_user(username, email, password)

    def create_tweet(self, user, content=None):
        if content is None:
            content = 'this is default content'
        return Tweet.objects.create(user=user, content=content)

    def create_comment(self, user, tweet, content=None):
        if content is None:
            content = 'default comment content'
        return Comment.objects.create(user=user, tweet=tweet, content=content)
