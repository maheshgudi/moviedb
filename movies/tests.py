import json

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token

from .models import Movie, Genre


class TestUserRegistration(TestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        User.objects.all().delete()

    def test_user_registration(self):
        """ Test user successful registration """
        response = self.client.post(
            reverse('movies:register_user'),
            data={'username': 'test_username', 'email': 'test@mail.com',
                  'password': 'test_password', 'first_name': 'test_ft_name',
                  'last_name': 'test_lt_name'}
        )
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data["status"])
        self.assertEqual(response_data["message"], "User created successfully")

    def test_failed_user_registration(self):
        """ Test user failed registration """
        response = self.client.post(
            reverse('movies:register_user'),
            data={'username': 'test', 'email': 'test@mail.com',
                  'first_name': 'test_ft_name', 'last_name': 'test_lt_name'}
            )
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_data["status"])
        self.assertEqual(response_data["password"][0],
                         "This field is required.")


class TestMovie(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_admin", password="test_admin_password",
            email="test_admin@mail.com"
        )
        self.token = Token.objects.create(user=self.user)
        self.grp = Group.objects.create(name="Administrator")
        self.post_movie_data = {
            "99popularity": 80, "director": "Test Director 1",
            "genre": ["Adventure", " Family"],
            "imdb_score": 8.0, "name": "Test Movie 1"
        }
        self.test_movie_data = {
            "popularity": 80, "director": "Test Director 2",
            "imdb_score": 8.0, "name": "Test Movie 2"
        }
        self.added_movie = Movie.objects.create(**self.test_movie_data)
        genres = Genre.objects.filter(
            name__in=["Adventure", "Family"]).values_list("id", flat=True)
        self.added_movie.genre.add(genres)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        Movie.objects.all().delete()
        Group.objects.all().delete()

    def test_failed_post_new_movie_no_auth(self):
        """ Test add new movie fail with no authentication """

        response = self.client.post(
            reverse('movies:movie'), data=self.post_movie_data
        )
        response_data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"],
                         "Unauthorized access")

    def test_add_new_post_failed_not_admin(self):
        response = self.client.post(
            reverse('movies:movie'), data=self.post_movie_data
        )
        response_data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_data["status"])
        self.assertEqual(response_data["message"], "Unauthorized access")

    def test_add_new_movie_success(self):
        self.grp.user_set.add(self.user)
        response = self.client.post(
            reverse('movies:movie'), data=self.post_movie_data
        )
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data["status"])
        self.assertEqual(response_data["data"][0]["name"], "Test Movie 1")

    def test_get_movie(self):
        self.grp.user_set.add(self.user)
        response = self.client.get(
            reverse('movies:movie', args=[self.added_movie.movie_id])
        )
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data["status"])
        self.assertEqual(response_data["data"]["name"], "Test Movie 2")

    def test_update_movie(self):
        self.grp.user_set.add(self.user)
        self.test_movie_data["name"] = "Test Movie 3"
        self.test_movie_data["genres"] = ["Family", "Adventure"]
        response = self.client.put(
            reverse('movies:movie', args=[self.added_movie.movie_id]),
            data=self.test_movie_data
        )
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data["status"])
        self.assertEqual(response_data["data"]["name"], "Test Movie 3")

    def test_search_movie(self):
        response = self.client.get(
            "{0}?name=Test".format(reverse('movies:search'))
        )
        response_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data["status"])
        self.assertEqual(response_data["data"][0]["name"], "Test Movie 2")
