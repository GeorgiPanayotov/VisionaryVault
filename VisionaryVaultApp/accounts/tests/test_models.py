from django.test import TestCase
from VisionaryVaultApp.accounts.models import CustomUser, Profile
from django.utils import timezone

"""Creating test user for the CustomUser model."""

class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='00000000A'
        )

    """Testing if a user is correctly created and has the expected attributes."""
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')


"""The UserProfileSignalIntegrationTests focuses on interaction between CustomUser and Profile:
User Creation,
Profile Existence, 
Profile Instance Check,
Field Validations, 
"""


class UserProfileSignalIntegrationTests(TestCase):
    """Testing if a profile is created after a new user is created."""
    def test_profile_created_on_user_creation(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='newuser@example.com',
            password='00000000A',
            first_name='Jane',  # Adding first_name
            last_name='Doe'  # Adding last_name
        )

        # Check if the profile was created
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)

        # Check that the profile fields are correctly set
        self.assertEqual(user.profile.first_name, 'Jane')  # Confirm first name
        self.assertEqual(user.profile.last_name, 'Doe')  # Confirm last name

        # Optionally, check other default values if necessary
        self.assertEqual(user.profile.date_of_birth, None)


