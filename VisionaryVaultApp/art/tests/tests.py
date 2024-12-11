import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from VisionaryVaultApp.art.models import ArtPiece, Category
from VisionaryVaultApp.art.forms import ArtPieceForm
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class ArtPieceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpassword0')
        self.category, created = Category.objects.get_or_create(category_name='Other')
        self.art_piece = ArtPiece.objects.create(
            user=self.user,
            title='Test Art',
            art_image='path/to/image.jpg',
            description='A beautiful painting.',
            categories=self.category,
            price=10.00
        )

    def test_art_piece_creation(self):
        art_piece = self.art_piece
        self.assertEqual(art_piece.title, 'Test Art')
        self.assertEqual(art_piece.price, 10.00)

    def test_likes_count(self):
        art_piece = self.art_piece
        self.assertEqual(art_piece.likes_count(), 0)


class ArtGalleryViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpassword0')
        self.client.login(username='testuser', password='Testpassword0')
        self.category = Category.objects.create(category_name='Painting')
        self.art_piece = ArtPiece.objects.create(
            user=self.user,
            title='Test Art',
            art_image='path/to/image.jpg',
            description='A beautiful painting.',
            categories=self.category,
            price=10.00
        )

    def test_art_gallery_list_view(self):
        url = reverse('art_gallery_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'art/art_gallery_list.html')
        self.assertContains(response, 'Test Art')

    def test_art_piece_create_view(self):
        url = reverse('upload_art')

        test_image_path = os.path.join(
            os.path.dirname(__file__),
            '../..',
            '..',
            'static',
            'images',
            'van_gogh_bg.jpg'
        )

        with open(test_image_path, 'rb') as img_file:
            image_file = SimpleUploadedFile(
                name='test_image.jpg',
                content=img_file.read(),
                content_type='image/jpeg'
            )

        response = self.client.post(url, {
            'title': 'New Art',
            'art_image': image_file,
            'description': 'A new painting.',
            'categories': self.category.id,
            'price': 15.00
        })

        self.assertRedirects(response, reverse('art_gallery_list'))
        self.assertEqual(ArtPiece.objects.last().title, 'New Art')

    def test_art_piece_detail_view(self):

        url = reverse('art_piece_detail', args=[self.art_piece.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'art/art_piece_detail.html')
        self.assertContains(response, 'A beautiful painting.')


class ArtPieceFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Testpassword1'
        )

        self.category = Category.objects.create(category_name='Other')

    def test_art_piece_form_with_invalid_data(self):
        form_data = {
            'title': '',
            'art_image': '',
            'description': '',
            'categories': '',
            'price': '',
        }

        form = ArtPieceForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


"""Integration test checking for: 
User Authentication, 
Category Creation, 
Image File Handling, 
Form Submission, 
Database Interaction, 
Verification of Redirection,
Rendering the View,
Template Verification"""


class ArtGalleryIntegrationTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Testpassword1'
        )
        self.client.login(username='testuser', password='Testpassword1')  # Login the user

        # Create a category for the art piece
        self.category = Category.objects.create(category_name='Other')

    def test_create_art_piece_and_view_in_gallery(self):
        static_image_path = os.path.join(
            os.path.dirname(__file__),
            '../..',
            '..',
            'static',
            'images',
            'van_gogh_bg.jpg'
        )

        # Open the image file for upload
        with open(static_image_path, 'rb') as img_file:
            image_file = SimpleUploadedFile(
                name='van_gogh_bg.jpg',
                content=img_file.read(),
                content_type='image/jpeg'
            )

            # Step 1: Submit the art piece creation form
            response = self.client.post(reverse('upload_art'), {
                'title': 'New Art',
                'art_image': image_file,
                'description': 'A new painting.',
                'categories': self.category.id,  # Valid category ID
                'price': 15.00,
            })

            # Assert the redirection after successful creation
            self.assertRedirects(response, reverse('art_gallery_list'))

            # Step 2: Check if the art piece was created successfully
            art_piece = ArtPiece.objects.last()
            self.assertIsNotNone(art_piece)  # Ensure the art piece exists
            self.assertEqual(art_piece.title, 'New Art')

            # Step 3: Verify that the art piece appears in the art gallery view
            gallery_response = self.client.get(reverse('art_gallery_list'))
            self.assertContains(gallery_response, 'New Art')

            # Optionally check if the correct template is used
            self.assertTemplateUsed(gallery_response, 'art/art_gallery_list.html')