from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    photo = models.ImageField(blank=True, upload_to='predict/post/%Y%m%d ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False, verbose_name='공개 여부')

    def __str__(self):
        return self.message
    class Meta:
        ordering = ['-id']
    def message_length(self):
        return len(self.message)

    message_length.short_description = "메세지 글자수"

class ImageUpload(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='', blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

class Predict_Result(models.Model):
    prediction = models.CharField(max_length=500)
    ground_truth = models.CharField(max_length=500)
    confidence = models.FloatField()
    is_correct = models.BooleanField()
