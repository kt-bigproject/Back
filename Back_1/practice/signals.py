import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from practice.models import PracticeContent
from practice.views import to_predict, to_mdb, to_txt, save_the_result, PredictAPIView


@receiver(post_save, sender=PracticeContent)
def process_upload_file(sender, instance, created, **kwargs):
    if created:
        # 완성
        to_txt('바른 먹거리 풀무원','00000066.png')
        to_mdb()
        to_predict('궁서 체')
        save_the_result('궁서 체')  

        # predict_url = 'http://localhost:8000/practice/predict/'  # PredictAPIView의 URL
        # response = requests.post(predict_url)