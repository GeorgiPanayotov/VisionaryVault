from rest_framework import serializers
from .models.comment import Comment
from .models.like import Like


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'art_piece', 'user', 'timestamp', 'status']
        read_only_fields = ['user', 'timestamp']

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Comment cannot be empty")
        return value


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'art_piece', 'user']

