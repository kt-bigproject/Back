from rest_framework import serializers
from .models import PracticeContent

class PracticeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeContent
        fields = '__all__'