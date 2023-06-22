from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from api.models import User

User = get_user_model()

class Blog(models.Model):
    RADIO_CHOICES = [
        ('normal', '일반'),
        ('announcement', '공지'),
    ]
    # 1. 게시글의 id 값
    id = models.AutoField(primary_key=True, null=False, blank=False)
    # 2. 일반글 / 공지글 선택
    radio_field = models.CharField(max_length=20, choices=RADIO_CHOICES, default='normal')
    # 3. 제목
    title = models.CharField(max_length=100)
    # 4. 작성일
    created_at = models.DateTimeField(auto_now_add=True)
    # 5. 작성자
    user = models.ForeignKey(User, related_name='%(class)s_blog', null=True, blank=True, on_delete=models.CASCADE)
    # user = models.CharField(max_length=100, null=True, blank=True)
    body = models.TextField()
    file = models.FileField(upload_to='font_data_uploads/', null=True, blank=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    blog = models.ForeignKey(Blog, null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='%(class)s_comment', null=False, blank=False, on_delete=models.CASCADE)
    # user = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateField(auto_now_add=True, null=False, blank=False)
    comment = models.TextField()
    file = models.FileField(upload_to='fonts/', null=True, blank=True)

    def __str__(self):
        return self.comment

