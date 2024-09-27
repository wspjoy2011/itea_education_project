from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from movies.models import (
    Certification,
    Genre,
    Director,
    Star,
    Movie,
    MovieGenre,
    MovieStar,
    MovieDirector
)

User = get_user_model()


class MovieListApiTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = User.objects.create_superuser(
            email='adminuser@example.com',
            username='adminuser',
            password='Testpassword1!',
            first_name='Admin',
            last_name='User'
        )
        cls.regular_user = User.objects.create_user(
            email='regular_user@example.com',
            username='regular_user',
            password='Testpassword1!',
            first_name='Regular',
            last_name='User'
        )
        cls.certification = Certification.objects.create(name='PG-13')
        cls.genre = Genre.objects.create(name='Action')
        cls.director = Director.objects.create(name='Director One')
        cls.star = Star.objects.create(name='Star One')

    def setUp(self):
        self.client = APIClient()
        self.token = self.get_token_for_user(user=self.admin_user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.movie = Movie.objects.create(
            name='Test Movie',
            year=2000,
            time=90,
            imdb=7.8,
            votes=10000,
            meta_score=75.0,
            certification=self.certification,
            description='Test movie description'
        )

        MovieStar.objects.create(movie=self.movie, star=self.star)
        MovieGenre.objects.create(movie=self.movie, genre=self.genre)
        MovieDirector.objects.create(movie=self.movie, director=self.director)

        self.url = reverse('api:api_movies_list')

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token

    def test_get_movie_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.movie.name)

    def test_post_movie(self):
        data = {
            'name': 'New Movie',
            'year': 2000,
            'time': 90,
            'imdb': 7.8,
            'votes': 10000,
            'meta_score': 75.0,
            'description': 'New movie description',
            'certification_id': self.certification.id,
            'genre_ids': [self.genre.id],
            'director_ids': [self.director.id],
            'star_ids': [self.star.id]
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(response.data['result']['name'], data['name'])

    def test_invalid_post_movie(self):
        data = {
            'name': '',
            'year': 2000,
            'time': 90,
            'imdb': 7.8,
            'votes': 10000,
            'meta_score': 75.0,
            'description': 'New movie description',
            'certification_id': self.certification.id,
            'genre_ids': [self.genre.id],
            'director_ids': [self.director.id],
            'star_ids': [self.star.id]
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['errors'])

    def test_non_admin_post_movie(self):
        data = {
            'name': 'New Movie',
            'year': 2000,
            'time': 90,
            'imdb': 7.8,
            'votes': 10000,
            'meta_score': 75.0,
            'description': 'New movie description',
            'certification_id': self.certification.id,
            'genre_ids': [self.genre.id],
            'director_ids': [self.director.id],
            'star_ids': [self.star.id]
        }

        token = self.get_token_for_user(user=self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MovieDetailAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = User.objects.create_superuser(
            email='adminuser@example.com',
            username='adminuser',
            password='Testpassword1!',
            first_name='Admin',
            last_name='User'
        )
        cls.regular_user = User.objects.create_user(
            email='regular_user@example.com',
            username='regular_user',
            password='Testpassword1!',
            first_name='Regular',
            last_name='User'
        )
        cls.certification = Certification.objects.create(name='PG-13')
        cls.genre = Genre.objects.create(name='Action')
        cls.director = Director.objects.create(name='Director One')
        cls.star = Star.objects.create(name='Star One')

    def setUp(self):
        self.client = APIClient()

        self.movie = Movie.objects.create(
            name='Test Movie',
            year=2000,
            time=90,
            imdb=7.8,
            votes=10000,
            meta_score=75.0,
            certification=self.certification,
            description='Test movie description'
        )

        MovieStar.objects.create(movie=self.movie, star=self.star)
        MovieGenre.objects.create(movie=self.movie, genre=self.genre)
        MovieDirector.objects.create(movie=self.movie, director=self.director)

        self.url = reverse('api:api_movies_detail', args=[self.movie.uuid])

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token

    def test_get_movie_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['name'], self.movie.name)

    def test_patch_update_movie_as_admin(self):
        token = self.get_token_for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {'name': 'Updated movie', 'year': 2022}

        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.name, data['name'])

    def test_patch_update_movie_as_non_admin(self):
        token = self.get_token_for_user(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {'name': 'Updated movie', 'year': 2022}

        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_movie_as_non_admin(self):
        token = self.get_token_for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(uuid=self.movie.uuid).exists())
