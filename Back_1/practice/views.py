from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PracticeContentSerializer
from .models import PracticeContent

class PracticeContentView(viewsets.ModelViewSet):
    serializer_class = PracticeContentSerializer
    queryset = PracticeContent.objects.all()
    
from .serializers import SentenceContentSerializer
from .models import SentenceContent

class SentenceContentView(viewsets.ModelViewSet):
    serializer_class = SentenceContentSerializer
    queryset = SentenceContent.objects.all()