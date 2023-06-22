from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    realname = models.CharField(max_length=100)
    profile_image = models.URLField(null=True, blank=True)
    user_type = models.CharField(max_length=20)
    kakao_id = models.BigIntegerField()

    def __str__(self):
        return self.user.username