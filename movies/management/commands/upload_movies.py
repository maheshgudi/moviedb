'''
   This command creates movies from a JSONified File.
'''
# Standard Imports
import json

# Django Imports
from django.core.management.base import BaseCommand, CommandError

# Local Imports
from movies.models import Movie, Genre


class Command(BaseCommand):
    help = 'Add movies to the database.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('movie_file', nargs='*', type=str)

    def handle(self, *args, **options):
        file = options.get("movie_file")[1]
        print(file)
        with open(file, 'r') as movie_file:
            json_movies = movie_file.read()
            movies = json.loads(json_movies)
            movie_data = {}
            for movie in movies:
                genre_list = movie.get('genre')
                movie, created = Movie.objects.get_or_create(
                    name=movie.get('name'), 
                    director=movie.get('director'),
                    imdb_score=movie.get('imdb_score'),
                    popularity=movie.get('99popularity')
                    )
                genres = []
                for name in genre_list:
                    name = name.strip()
                    genre, created = Genre.objects.get_or_create(name=name)
                    genres.append(genre)
                movie.genre.add(*genres)
