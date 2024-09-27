import datetime

from django.contrib.auth import get_user_model, authenticate, get_user
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Profile

User = get_user_model()


class UserAuthViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'email': 'regular_user@example.com',
            'username': 'regular_user',
            'password': 'Testpassword1!',
            'first_name': 'Regular',
            'last_name': 'User'
        }

        self.profile_data = {
            'avatar': 'path_to_folder/',
            'gender': 'm',
            'date_of_birth': datetime.datetime.today() - datetime.timedelta(days=31 * 365 * 25),
            'info': 'Test info'

        }

        self.test_user = User.objects.create_user(**self.user_data)
        self.test_user_profile = Profile.objects.create(user=self.test_user, **self.profile_data)

        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.index_url = reverse('blog:post_list')

    def test_user_login_view(self):
        response = self.client.post(
            self.login_url,
            {'email': self.user_data['email'], 'password': self.user_data['password']},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

        user = get_user(self.client)
        self.assertEqual(user, self.test_user)

    def test_user_already_login(self):
        self.client.login(
            username=self.user_data["email"], password=self.user_data["password"]
        )

        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

        response = self.client.get(self.login_url, follow=True)
        user = get_user(self.client)

        self.assertTrue("You&#x27;re already logged in" in response.content.decode())
        self.assertTrue(user.username in response.content.decode())

    def test_user_logout(self):
        self.client.login(
            username=self.user_data["email"], password=self.user_data["password"]
        )

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

        user = get_user(self.client)
        self.assertTrue(user.is_anonymous)
