# serializer.py
from .models import Blog, Comment
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username', allow_null=True)
    num_comments = serializers.IntegerField(read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'radio_field', 'title', 'created_at', 'user', 'body', 'file', 'user_id', 'num_comments', 'views']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Comment
        fields = '__all__'