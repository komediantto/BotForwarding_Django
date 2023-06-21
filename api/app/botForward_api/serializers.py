from rest_framework import serializers
from .models import Post, Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'is_verified', 'media', 'target_channel']
