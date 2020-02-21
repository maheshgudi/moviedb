from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Movie


from .serializers import MovieSerializer


class MovieList(APIView):
    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class AddMovie(APIView):

    def post(self, request, format=None):
        try:
            serializer = MovieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    def get(self, request, pk, format=None):
        movie = Movie.objects.get(id=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        movie = Movie.objects.get(id=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        movie = Movie.objects.get(id=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminPanel(APIView):
    def post(self, request):
        pass
