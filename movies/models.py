import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models

from .search_query_builder import build_query



class MovieManager(models.Manager):

    def search_movie_by_field(self, **kwargs):
        query = build_query(kwargs)
        if query:
            try:
                return self.filter(**query)
            except ValueError:
                raise


class Movie(models.Model):

    name = models.TextField()
    director = models.CharField(max_length=100)
    imdb_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    popularity = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    genre = models.ManyToManyField("Genre")
    movie_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    objects = MovieManager()

    def __str__(self):
        return f"Movie: {self.name}"

    @property
    def genres(self):
        return self.genre.values_list('name', flat=True)


class Genre(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Genre: {self.name}"
