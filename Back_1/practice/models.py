from django.db import models

# Create your models here.
class PracticeContent(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    font = models.CharField(max_length=30, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="uploads")
    
class SentenceContent(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    sentence = models.CharField(max_length=30, null=True)