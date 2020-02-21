from rest_framework import serializers

from .models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ["name",]


class MovieSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = ["name", "director", "imdb_score", "popularity", "genre"]
