from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    games = models.ManyToManyField('Game', through='GameGenre', through_fields=('genre', 'game'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Жанры'


class Publisher(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    director = models.CharField(max_length=50)
    founder = models.CharField(max_length=50)
    founded = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Издатели'


class GameStudio(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    image = models.ImageField()
    founded = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Игровые студии'


class Game(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    released = models.IntegerField()
    image = models.ImageField()
    metacritic_rating = models.IntegerField()

    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, blank=False, null=False)
    game_studio = models.ForeignKey('GameStudio', on_delete=models.CASCADE, blank=False, null=False)
    genres = models.ManyToManyField('Genre', through='GameGenre', through_fields=('game', 'genre'))
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Игры'


class GameGenre(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, blank=False, null=False)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game.name + " - " + self.genre.name

    class Meta:
        verbose_name_plural = 'Жанры для игр'
        constraints = [
            models.UniqueConstraint(fields=['game', 'genre'], name='unique_game_genre')
        ]


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, blank=False, null=False)
    rating = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Пользователь " + self.user.username + " оценил игру " + self.game.name + " в " + str(self.rating) + "/10"

    class Meta:
        verbose_name_plural = 'Оценки пользователей'
        constraints = [
            models.UniqueConstraint(fields=['user', 'game'], name='unique_game_user_rating')
        ]
