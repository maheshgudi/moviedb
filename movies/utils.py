# Standard Imports
import json
from json import JSONDecodeError
# Local Imports
from movies.models import Movie, Genre


class MovieUtils:
    def __init__(self, movies_data):
        self.movies_data = movies_data

    def add_movies(self):
        if isinstance(self.movies_data, str):
            try:
                movies = json.loads(self.movies_data)
            except JSONDecodeError:
                return False, []
        elif isinstance(self.movies_data, dict):
            movies = [self.movies_data]
        else:
            movies = self.movies_data
        added_movies = []
        for movie in movies:
            try:
                genre_list = movie.get('genre') or movie.get("genres")
                movie, created = Movie.objects.get_or_create(
                    name=movie.get('name'),
                    director=movie.get('director'),
                    imdb_score=movie.get('imdb_score'),
                    popularity=movie.get('99popularity') or movie.get("popularity")
                    )
                genres = []
                for name in genre_list:
                    name = name.strip()
                    genre, created = Genre.objects.get_or_create(name=name)
                    genres.append(genre)
                movie.genre.add(*genres)
                added_movies.append(movie)
            except:
                return False, []
        return True, added_movies
