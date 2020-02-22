from django.urls import path, re_path

from . import views

from rest_framework.schemas import get_schema_view

urlpatterns = [
	path('', get_schema_view(
        title="Django Movie DB",
        description="API for searching, adding, editing and deleting movies",
        version=1.0
    ), name='openapi-schema.yml'),

    path('allmovies/', views.MovieList.as_view(), name="movies"),
    path('movie/<uuid:movie_id>/', views.MovieDetail.as_view(), name="movie"),
    path('movie/', views.MovieDetail.as_view(), name="movie"),
    path('search/', views.SearchMovie.as_view(), name="search"),
    path('register/', views.Register.as_view(), name="register_user"),

]
