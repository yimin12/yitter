from rest_framework import serializers
from newsfeeds.models import NewsFeed
from tweets.api.serializers import TweetSerializer

class NewsFeedSerializer(serializers.Serializer):
    tweet = TweetSerializer()
    created_at = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_tweet(self, obj):
        return TweetSerializer(obj.cached_tweet, context=self.context).data

    def get_created_at(self, obj):
        return obj.created_at

    class Meta:
        model = NewsFeed
        fields = ('id', 'created_at', 'user', 'tweet')