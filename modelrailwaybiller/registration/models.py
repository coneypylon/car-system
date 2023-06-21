from django.contrib.auth.models import AbstractUser
from django.db import models

class RailUser(AbstractUser):
    # here's where the layout number comes from
    layout_id = models.IntegerField()
    # we'll use an other_layout_ids list later - layout_id is the active layout
    
    class Meta:
        # Set the table name for the custom user model
        db_table = 'auth_user'


