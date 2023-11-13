from django.test import TestCase, Client
from users.models import Users, Profiles, Tokens
from django.urls import reverse
from django.utils import timezone


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create_user(
            username="testuser", email="testuser@mail.com", password="qwerty123"
        )
        Profiles.objects.create(user=self.user)
        Tokens.objects.create(user=self.user)

    def test_user_registration(self):
        response = self.client.post(reverse("registration"), {
            'username': 'testuser1',
            'email': 'testuser1@mail.com',
            'password': 'qwerty12345',
            'confirm_password': 'qwerty12345'
        })
        self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_username(self):
        response = self.client.post(reverse("registration"), {
            'username': 'testuser',
            'email': 'testuser@mail.com',
            'password': 'qwerty12345',
            'confirm_password': 'qwerty12345'
        })
        self.assertNotEqual(response.status_code, 201)
 
    def test_user_login(self):
        response = self.client.post(reverse("login"), {
            'username_email': 'testuser',
            'password': 'qwerty123'
        })
        self.assertEqual(response.status_code, 200)

    def test_user_login_wrong_password(self):
        response = self.client.post(reverse("login"), {
            'username_email': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertNotEqual(response.status_code, 200)

    def test_user_logout(self):
        response = self.client.post(reverse("login"), {
            'username_email': 'testuser',
            'password': 'qwerty123'
        })
        token = response.data['access_token']
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        
        response = self.client.post(reverse("auth_logout"))

        self.assertEqual(response.status_code, 200)

        token = Tokens.objects.get(user=self.user)
        self.assertIsNone(token.access_token)
        self.assertIsNone(token.refresh_token)

    def test_registration_with_get_method(self):
        response = self.client.get(reverse("registration"))
        self.assertEqual(response.status_code, 405)

    def test_login_with_put_method(self):
        response = self.client.put(reverse("login"))
        self.assertEqual(response.status_code, 405)

    def test_logout_with_delete_method(self):
        response = self.client.post(reverse("login"), {
            'username_email': 'testuser',
            'password': 'qwerty123'
        })
        token = response.data['access_token']
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'

        response = self.client.delete(reverse("auth_logout"))
        self.assertEqual(response.status_code, 405)


