# serializer.py
from .models import Blog, Comment
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username', allow_null=True)
    num_comments = serializers.IntegerField(read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'radio_field', 'title', 'created_at', 'user', 'body', 'file', 'user_id', 'num_comments', 'views']

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    replies = RecursiveField(many=True, read_only=True)
    # replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('replies',)

    # def get_replies(self, obj):
    #     if obj.replies:
    #         return CommentSerializer(obj.replies.all(), many=True).data
    #     return None