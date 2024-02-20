from django.test import TestCase, RequestFactory
from django.urls import reverse
from network.models import User, Profile, Post

from network.views import edit_post

# Create your tests here.

class Edit_Post_Test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create User
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='12345@Test')
        profile1 = Profile.objects.get(user=self.user1)        
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='12345@Test')

        # Create test post
        new_post = Post(owner=profile1, text="Test post.")
        new_post.save()
        self.post_id = Post.objects.first().id

        # Create request data
        self.data = {
            'id': self.post_id,
            'action': 'edit',
            'text': 'Edited post.'
        }

    def test_edit_post(self):
        """Test valid edit post request"""

        # Create request
        self.client.login(username='testuser1', password='12345@Test')
        request = self.factory.post(reverse('edit_post'), self.data, content_type='application/json')
        request.user = self.user1
        
        # Submit to edit_post view and assert response
        response = edit_post(request)
        self.assertEqual((response.status_code), (200), response.content)

        # Check if edit saved in database
        target_post = Post.objects.get(pk=self.post_id)
        self.assertEqual(target_post.text, 'Edited post.')

    def test_edit_unowned(self):
        """Test valid edit post request"""

        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request = self.factory.post(reverse('edit_post'), self.data, content_type='application/json')
        request.user = self.user2
        
        # Submit to edit_post view and assert response
        response = edit_post(request)
        self.assertEqual((response.status_code), (400), response.content)

        # Check if edit not saved in database
        target_post = Post.objects.get(pk=self.post_id)
        self.assertEqual(target_post.text, 'Test post.')

    def test_edit_invalid(self):
        """Test valid edit post request"""

        request_data = {
            'foo':'bar',
            'baz': True
        }

        # Create request
        self.client.login(username='testuser1', password='12345@Test')
        request = self.factory.post(reverse('edit_post'), request_data, content_type='application/json')
        request.user = self.user1
        
        # Submit to edit_post view and assert response
        response = edit_post(request)
        self.assertEqual((response.status_code), (400), response.content)

    def test_edit_invalid_id(self):
        """Test valid edit post request"""

        # Get pk of last post item
        last_post = Post.objects.order_by('pk').last()
        request_data = {
            **self.data,
            'id': last_post.id + 1
        }

        # Create request
        self.client.login(username='testuser1', password='12345@Test')
        request = self.factory.post(reverse('edit_post'), request_data, content_type='application/json')
        request.user = self.user1
        
        # Submit to edit_post view and assert response
        response = edit_post(request)
        self.assertEqual((response.status_code), (400), response.content)
