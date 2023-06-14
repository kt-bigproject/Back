# serializer.py
from .models import Blog, Comment
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username', allow_null=True)
    class Meta:
        model = Blog
        fields = ['id', 'title', 'created_at', 'user', 'body', 'image']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'user', 'created_at', 'comment']