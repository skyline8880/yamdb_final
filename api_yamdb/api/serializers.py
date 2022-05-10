import logging

# from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

# User = get_user_model()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s, %(message)s, %(name)s",
)

logger = logging.getLogger(__name__)


class EmailUsernameSerializer(serializers.Serializer):
    """
    Сериализатор email и username.
    Отправка на email confirmation code
    """

    email = serializers.EmailField(
        required=True,
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
    )

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Пользователь с email \'{email}\' уже существует.'
            )

        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь \'{username}\' уже существует.'
            )

        return data

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('username "me" is not allowed!')
        return value


class UserConfirmationCodeSerializer(serializers.Serializer):
    """
    Сериализатор username и confirmation_code.
    Выдача JWT-токена
    """

    confirmation_code = serializers.SlugField(required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError(
                'Сonfirmation code is incorrect'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if not self.context['request'].user.is_admin and key == 'role':
                value = self.context['request'].user.role
            setattr(instance, key, value)
        instance.save()
        return instance


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=20)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )
        model = Title


class ReviewCreateSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        title = get_object_or_404(
            Title,
            id=self.context['request'].parser_context['kwargs']['title_id']
        )
        author = self.context['request'].user
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError('один автор - одно'
                                              'произведение-одно ревью!')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'pub_date', 'text')
        model = Comment
