from django.test import TestCase, RequestFactory
from django.urls import reverse
from network.models import User, Profile, Post

from network import views

# Create your tests here.

class Like_Post_Test(TestCase):
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
            'action': 'like',
            'modifier': True
        }


    def test_like_post(self):
        """Test liking a post."""

        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request = self.factory.post(reverse('like_post'), self.data, content_type='application/json')
        request.user = self.user2
        
        # Submit to like_post view and assert response
        response = views.like_post(request)
        self.assertEqual((response.status_code), (200), response.content)

        # Check if like saved in database
        target_post = Post.objects.get(pk=self.post_id)
        self.assertEqual(target_post.likes.count(), 1)

    def test_like_own(self):
        """Test liking your own post."""
        
        # Create request
        self.client.login(username='testuser1', password='12345@Test')
        request = self.factory.post(reverse('like_post'), self.data, content_type='application/json')
        request.user = self.user1
        
        # Submit to like_post view and assert response
        response = views.like_post(request)
        self.assertEqual(response.status_code, 400, response.content)

        # Check if like not saved in database
        target_post = Post.objects.get(pk=self.post_id)
        self.assertEqual(target_post.likes.count(), 0)

    def test_unlike(self):
        """Test unliking an already liked post."""

        # Add user 2 to likes
        sample_post = Post.objects.get(pk=self.post_id)
        sample_post.likes.add(self.user2.profile)
        sample_post.save()

        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request_data = {
            **self.data,
            'modifier': False
        }
        request = self.factory.post(reverse('like_post'), request_data, content_type='application/json')
        request.user = self.user2
        
        # Submit to like_post view and assert response
        response = views.like_post(request)
        self.assertEqual(response.status_code, 200, response.content)

        # Check if like saved in database
        target_post = Post.objects.get(pk=self.post_id)
        self.assertEqual(target_post.likes.count(), 0)

    def test_submit_invalid(self):
        """Test submitting an invalid JSON"""
        
        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request_data = {
            'foo':'bar',
            'baz': True
        }
        request = self.factory.post(reverse('like_post'), request_data, content_type='application/json')
        request.user = self.user2
        
        # Submit to like_post view and assert response
        response = views.like_post(request)
        self.assertEqual(response.status_code, 400, response.content)

    def test_like_invalid(self):
        """Test liking an invalid post id."""
        
        # Get pk of last post item
        last_post = Post.objects.order_by('pk').last()

        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request_data = {
            **self.data,
            'id': last_post.id + 1,
        }
        request = self.factory.post(reverse('like_post'), request_data, content_type='application/json')
        request.user = self.user2
        
        # Submit to like_post view and assert response
        response = views.like_post(request)
        self.assertEqual((response.status_code), (400), response.content)