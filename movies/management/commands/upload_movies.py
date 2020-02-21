'''
   This command creates movies from a JSONified File.
'''
# Django Imports
from django.core.management.base import BaseCommand, CommandError

# Local Imports
from movies.utils import MovieUtils


class Command(BaseCommand):
    help = 'Add movies to the database.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('movie_file', nargs='*', type=str)

    def handle(self, *args, **options):
        file = options.get("movie_file")[1]
        with open(file, 'r') as movie_file:
            movies_file = movie_file.read()
            movies = MovieUtils(movies_file)
            movies.add_movies()
        print("Added Movies")