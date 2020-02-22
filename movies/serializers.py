from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User

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
        fields = ["movie_id","name", "director", "imdb_score", "popularity", "genres"]


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="Email already exists"
            )
        ]
    )
    username = serializers.CharField(
        validators=[
        UniqueValidator(
            queryset=User.objects.all(), message="Username already exists"
            )
        ]
    )
    password = serializers.CharField(min_length=6)
    first_name = serializers.CharField(
        required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        required=False, allow_blank=True
    )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password")

# class TokenSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         validators=[
#         UniqueValidator(
#             queryset=User.objects.all(), message="Username already exists"
#             )
#         ]
#     )
#     password = serializers.CharField(min_length=6)

#     class Meta:
#         model = tOKE
#         fields = ("username", "email", "first_name", "last_name", "password")