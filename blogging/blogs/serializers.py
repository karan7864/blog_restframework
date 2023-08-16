# appname/serializers.py

from rest_framework import serializers
from .models import BlogPost, Comment, CommentReaction, UserProfile


class CommentReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReaction
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    reactions = CommentReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
