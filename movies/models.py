from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models



class Movie(models.Model):

    name = models.TextField()
    director = models.CharField(max_length=100)
    imdb_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    popularity = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    genre = models.ManyToManyField("Genre")

    def __str__(self):
        return f"Movie: {self.name}"


class Genre(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Genre: {self.name}"
