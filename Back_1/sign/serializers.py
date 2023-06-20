from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            nickname = validated_data['nickname'],
            email = validated_data['email'],
            password = validated_data['password'],
        )
        return user
    class Meta:
        model = User
        fields = ['nickname', 'email', 'password']