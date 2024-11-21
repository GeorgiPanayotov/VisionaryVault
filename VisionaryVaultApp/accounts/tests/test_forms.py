from django.test import TestCase
from VisionaryVaultApp.accounts.forms import UserRegistrationForm, EmailChangeForm
from VisionaryVaultApp.accounts.models import CustomUser


class UserRegistrationFormTests(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        CustomUser.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='00000000A'
        )
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This email is already being used.'])


class EmailChangeFormTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='00000000A'
        )

    def test_email_change_form(self):
        form = EmailChangeForm(data={'email': 'new_email@example.com'})
        self.assertTrue(form.is_valid())
