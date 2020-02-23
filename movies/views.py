from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    authentication_classes, permission_classes
)
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from .models import Movie
from .utils import MovieUtils

from .serializers import MovieSerializer, RegistrationSerializer


class MovieList(APIView):
    """API to get all movies in the database."""

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


@authentication_classes(())
@permission_classes(())
class SearchMovie(APIView):
    def get(self, request):
        query = request.GET.dict()
        try:
            movies = Movie.objects.search_movie_by_field(**query)
        except ValueError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Bad Query Argument", "status": False})
        if movies:
            serializer = MovieSerializer(movies, many=True)
            context = {"status": True, "data": serializer.data}
            return Response(context)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Query parameter does not exist",
                      "status": False})


class MovieDetail(APIView):
    """ API only for admin to get, delete and update the movie info """

    GROUP_NAME = "Administrator"

    def verify_admin_user(self, user):
        context = {}
        group = get_object_or_404(Group, name=self.GROUP_NAME)
        if (user.is_anonymous or not
                group.user_set.filter(id=user.id).exists()):
            context.update({"status": False, "message": "Unauthorized access"})
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            context.update({"status": True})
            status_code = status.HTTP_200_OK
        return context, status_code 

    def get(self, request, movie_id=None):
        user = request.user
        context, status_code = self.verify_admin_user(user)
        if movie_id:
            if status_code == status.HTTP_200_OK:
                movie = get_object_or_404(Movie, movie_id=movie_id)
                serializer = MovieSerializer(movie)
                context["data"] = serializer.data
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            context["status"] = False
            context["message"] = "This requires a movie id"
        return Response(context, status=status_code)

    def post(self, request, movie_id=None):
        user = request.user
        context, status_code = self.verify_admin_user(user)
        if status_code == status.HTTP_200_OK:
            movieutils = MovieUtils(request.data)
            add_status, added = movieutils.add_movies()
            if add_status:
                serializer = MovieSerializer(movieutils.add_movies(), many=True)
                context["data"] = serializer.data
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                context["status"] = False
                context["message"] = "Unable to parse Json fields. Please check"
        return Response(context, status=status_code)

    def put(self, request, movie_id):
        user = request.user
        context, status_code = self.verify_admin_user(user)
        if status_code == status.HTTP_200_OK:
            movie = get_object_or_404(Movie, movie_id=movie_id)
            serializer = MovieSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context["data"] = serializer.data
            else:
                context["errors"] = serializer.errors
        return Response(context, status=status_code)

    def delete(self, request, movie_id):
        user = request.user
        context, status_code = self.verify_admin_user(user)
        if status_code == status.HTTP_200_OK:
            movie = get_object_or_404(Movie, movie_id=movie_id)
            context = {
            "status": True,
            "message": f"{movie.name} deleted successfully"
            }
            movie.delete()
        return Response(context, status=status_code)


@authentication_classes(())
@permission_classes(())
class Register(APIView):
    """ API to register user and generate token"""
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user_id=user.id)
            context = {
            "token": token.key,
            "status": True,
            "message": "User created successfully"
            }
        else:
            context = {"status": False}
            context.update(serializer.errors)
        return Response(context)
