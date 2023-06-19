from rest_framework import serializers
from .models import PracticeContent, SentenceContent, SyllableContent, WordContent , Predict_Result

class PracticeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeContent
        fields = '__all__'
        
class SentenceContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentenceContent
        fields = '__all__'
        
class SyllableContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyllableContent
        fields = '__all__'
        
class WordContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordContent
        fields = '__all__'
        
        
class MyPredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predict_Result
        fields ='__all__'