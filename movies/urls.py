from django.urls import path

from . import views

urlpatterns = [
    path('movies', views.MovieList.as_view(), name="movies"),
]
