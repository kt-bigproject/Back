# temp/serializer.py
from .models import Temp
from rest_framework import serializers

class TempSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username', allow_null=True)
    class Meta:
        model = Temp
        fields = ['id', 'title', 'created_at', 'user', 'body', 'image']