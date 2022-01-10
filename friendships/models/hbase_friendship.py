from django_hbase import models

class HBaseFollowing(models.HBaseModel):
    """
    Store people they follow from from_user_id, order it by from_user_id+created_at
    """
    # row key
    from_user_id = models.IntegerField(reverse=True)
    created_at = models.TimestampField()
    # column key
    to_user_id = models.IntegerField(column_family='cf')

    class Meta:
        table_name = 'yitter_followings'
        row_key = ('from_user_id', 'created_at')

class HBaseFollower(models.HBaseModel):
    """
    opposite concept for the above class
    """
    # row key
    to_user_id = models.IntegerField(reverse=True)
    created_at = models.TimestampField()
    # column key
    from_user_id = models.IntegerField(column_family='cf')

    class Meta:
        row_key = ('to_user_id', 'created_at')
        table_name = 'yitter_followers'