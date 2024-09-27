from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase

from accounts.forms import RegisterForm


class RegisterFormTestCase(TestCase):
    def setUp(self):
        self.form_data = {
            'email': 'regular_user@example.com',
            'username': 'regular_user',
            'password1': 'Testpassword1!',
            'password2': 'Testpassword1!',
            'first_name': 'Regular',
            'last_name': 'User',
            'agree_terms': True
        }

    def test_form_success(self):
        form = RegisterForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, get_user_model())

        self.assertTrue(
            authenticate(username=self.form_data['email'], password=self.form_data['password1'])
        )

    def test_form_lastname_invalid(self):
        self.form_data['last_name'] += '_'
        form = RegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['last_name'][0],
            f"{self.form_data['last_name']} contains non-english letters"
        )

    def test_form_username_invalid(self):
        self.form_data['username'] += '123'
        form = RegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0],
            f"{self.form_data['username']} contains non-english letters or characters other than underscore"
        )

    def test_form_unchecked_agree_checkbox(self):
        self.form_data['agree_terms'] = False
        form = RegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['agree_terms'][0],
            'This field is required.'
        )




















