from rest_framework import serializers

from posts.models import Comment, Group, Follow, Post, User


class BaseTextSerializer(serializers.ModelSerializer):
    """Base text serializer. Provides fields 'id', 'author', 'text'.
    Where 'author' is a read_only StringRelatedField.
    """
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = (
            'id', 'author', 'text'
        )


class PostSerializer(BaseTextSerializer):
    class Meta:
        fields = BaseTextSerializer.Meta.fields + (
            'pub_date', 'image', 'group'
        )
        model = Post


class CommentSerializer(BaseTextSerializer):
    class Meta:
        fields = BaseTextSerializer.Meta.fields + ('created', 'post')
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='You already follow this user'
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'You can not follow yourself')
        return data
