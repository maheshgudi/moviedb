from rest_framework.views import APIView

from .models import Movie

from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import MovieSerializer


class MovieList(APIView):
    def get(self, request, format=None):
        movies = Movie.objects.all().order_by("-popularity")
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class AdminPanel(APIView):
    def post(self, request):
        pass
