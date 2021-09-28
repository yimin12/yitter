from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet
# Create your models here.

class Comment(models.Model):
    """
    We only implement comment in easy way. The comment is under the tweets and
    we can not comment the other user's comment
    """
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # sort the comments under tweet with time order
        index_together = (('tweet', 'created_at'),)

    def __str__(self):
        return '{} - {} says {} at tweet'.format(
            self.created_at,
            self.user,
            self.content,
            self.tweet_id
        )