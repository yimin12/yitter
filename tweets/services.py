from tweets.models import tweet_photo, Tweet
from utils.redis_helper import RedisHelper
from yitter.cache import USER_TWEETS_PATTERN


class TweetService(object):

    @classmethod
    def create_photos_from_files(cls, tweet, files):
        photos = []
        for index, file in enumerate(files):
            photo = tweet_photo(
                tweet = tweet,
                user = tweet.user,
                file = file,
                order = index,
            )
            photos.append(photo)
        tweet_photo.objects.bulk_create(photos)

    @classmethod
    def get_cached_tweets(cls, user_id):
        queryset = Tweet.objects.filter(user_id=user_id).order_by('-created_at')
        key = USER_TWEETS_PATTERN.format(user_id=user_id)
        return RedisHelper.load_objects(key, queryset)

    @classmethod
    def push_tweet_to_cache(cls, tweet):
        queryset = Tweet.objects.filter(user_id=tweet.user_id).order_by('-created_at')
        key = USER_TWEETS_PATTERN.format(user_id=tweet.user_id)
        RedisHelper.push_object(key, tweet, queryset)