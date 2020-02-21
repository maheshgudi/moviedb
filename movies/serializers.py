from rest_framework import serializers

from .models import Movie, Genre


class MovieSerializer(serializers.ModelSerializer):

    genres = serializers.ListField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.director = validated_data.get('director', instance.director)
        instance.imdb_score = validated_data.get('imdb_score', instance.imdb_score)
        instance.popularity = validated_data.get('popularity', instance.popularity)
        genres = Genre.objects.filter(
            name__in=validated_data.get('genres')
        ).values_list("id", flat=True)
        instance.save()
        instance.genre.add(*genres)
        return instance

    class Meta:
        model = Movie
        fields = ["name", "director", "imdb_score", "popularity", "genres"]
