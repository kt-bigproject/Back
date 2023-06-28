from django.db import models



# Create your models here.
class PracticeContent(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    font = models.CharField(max_length=30, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='game')
    sentence = models.CharField(max_length=200, null=True)
    
class SyllableContent(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    syllable = models.CharField(max_length=30, null=True)
    
class WordContent(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    word = models.CharField(max_length=30, null=True)
    
class SentenceContent(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    sentence = models.CharField(max_length=30, null=True)
    
class Predict_Result(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.CharField(max_length=30, null=True)
    # stage = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # comment = models.CharField(max_length=500, null=True)
    score = models.FloatField()
    is_correct = models.BooleanField(null=True)

