from django.urls import path

from . import views

urlpatterns = [
    path('movies', views.MovieList.as_view(), name="movies"),
    path('movie/<int:pk>', views.MovieDetail.as_view(), name="movie"),
    path('search/', views.SearchMovie.as_view(), name="movie"),
    path('add/movie/', views.AddMovie.as_view(), name="add_movie"),
    
]
