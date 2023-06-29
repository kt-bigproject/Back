# serializer.py
from .models import Blog, Comment
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username', allow_null=True)
    num_comments = serializers.IntegerField(read_only=True)
    num_likes = serializers.IntegerField(read_only=True) 
    class Meta:
        model = Blog
        fields = ['id', 'title', 'created_at', 'user', 'body', 'image', 'user_id', 'num_comments', 'views', 'num_likes']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Comment
        fields = '__all__'