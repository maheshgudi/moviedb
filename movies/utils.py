# Standard Imports
import json
# Local Imports
from movies.models import Movie, Genre


class MovieUtils:
    def __init__(self, movies_data):
        self.movies_data = movies_data

    def add_movies(self): 
        movies = json.loads(self.movies_data)
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