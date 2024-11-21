from django.test import TestCase
from django.urls import reverse
from VisionaryVaultApp.accounts.models import CustomUser, Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()


class CustomLoginViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='ComplexPass123!'
        )

    def test_login_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username_or_email': 'testuser',
            'password': 'ComplexPass123!'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class RegisterViewTests(TestCase):

    def test_register_new_user(self):
        """Test that a new user can register successfully."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })

        # Check that the response redirects (to login page or any specified page after success)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful registration

        # Check if the user is actually created in the database
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())

        # Optionally, check for any success messages:
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)  # Ensure that there is a success message
        self.assertEqual(str(messages[0]), 'Account created successfully!')