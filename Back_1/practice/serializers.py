from rest_framework import serializers
from .models import PracticeContent, SentenceContent

class PracticeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeContent
        fields = '__all__'
        
class SentenceContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentenceContent
        fields = '__all__'