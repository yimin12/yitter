from django.contrib import admin
from tweets.models import Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    data_hierarchy = 'create_at'
    list_display = (
        'created_at',
        'user',
        'content',
    )

@admin.register(TweetPhoto)
class TweetPhotoAdmin(admin.ModelAdmin):
    list_display = (
        'tweet',
        'user',
        'file',
        'status',
        'has_deleted',
        'created_at',
    )
    list_filter = ('status', 'has_delete')
    date_hierarchy = 'created_at'