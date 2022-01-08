from rest_framework import serializers
from notifications.models import Notification
from accounts.api.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer()

    class Meta:
        model = Notification
        fields = (
            'id',
            'recipient',
            'actor_content_type',
            'actor_object_id',
            'verb',
            'action_object_content_type',
            'target_content_type',
            'target_object_id',
            'timestamp',
            'unread',
        )

class NotificationSerializerForUpdate(serializers.ModelSerializer):
    # BooleanField will convert true, false, "true", "fasle", "1", "0" to Boolean
    unread = serializers.BooleanField()

    class Meta:
        model = Notification
        fields = ('unread', )

    def update(self, instance, validate_data):
        instance.unread = validate_data['unread']
        instance.save()
        return instance