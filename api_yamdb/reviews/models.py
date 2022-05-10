from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='slug')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='slug')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Genre'


class Title(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='name')
    description = models.TextField(verbose_name='description')
    year = models.IntegerField()
    genre = models.ManyToManyField(
        'Genre',
        related_name='genre',
        verbose_name='genre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        null=True,
        verbose_name='category'
    )

    class Meta:
        ordering = ('name', 'year',)
        verbose_name = 'Title'


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title')
        ]

        ordering = ['pk']


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'pub_date', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['pk']
