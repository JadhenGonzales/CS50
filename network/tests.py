from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from .models import User, Profile, Post

from . import views

# Create your tests here.
class Create_Profile_Signal_Test(TestCase):

    def testCreateUser(self):
        """Test profile creation upon user creation."""
        self.user = User.objects.create_user(username='testuser1', email='test@example.com', password='12345@Test')
        self.profile = Profile.objects.get(user=self.user)
        self.assertEqual(self.profile.user.username, self.user.username)

class Login_Redirect_Test(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_with_anonymous_user(self):
        """Test if app redirects to proper login page"""
        post_data = {
            'post_content': 'Test post'
        }

        response = self.client.post(reverse('create_post'), data=post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('create_post'))


class Create_Post_Test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create and login User
        self.user = User.objects.create_user(username='testuser1', email='test@example.com', password='12345@Test')
        self.profile = Profile.objects.get(user=self.user)
        self.client.login(username='testuser1', password='12345@Test')

    def test_create(self):
        """Test submitting post to create_post"""

        # Submit POST request to view
        request_data = {
            'post_content': 'Test post'
        }
        request = self.factory.post(reverse('create_post'), data=request_data)
        request.user = self.user
        response = views.create_post(request)

        self.assertEqual(response.status_code, 201)

        # Check if comment exists in database
        post_exists = Post.objects.filter(
            owner=self.profile,
            text='Test post',
        ).exists()

        self.assertTrue(post_exists)

    def test_other_method(self):
        """Test submitting a post with GET method"""

        # Submit POST request to view
        request_data = {
            'post_content': 'Test post'
        }
        request = self.factory.get(reverse('create_post'), data=request_data)
        request.user = self.user
        response = views.create_post(request)

        self.assertEqual(response.status_code, 400)


class Like_Post_Test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create User
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='12345@Test')
        self.profile = Profile.objects.get(user=self.user1)        
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='12345@Test')

        # Create test post
        new_post = Post(owner=self.profile, text="Test post.")
        new_post.save()
        self.post_id = Post.objects.first().id

    def test_like_post(self):
        """Test liking a post."""

        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request_data = {
            'post_id': self.post_id,
            'like_status': True
        }
        request = self.factory.post(reverse('like_post'), request_data, content_type='application/json')
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
        request_data = {
            'post_id': self.post_id,
            'like_status': True
        }
        request = self.factory.post(reverse('like_post'), request_data, content_type='application/json')
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
            "post_id": self.post_id,
            "like_status": False
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
            'post_id': last_post.id + 1,
            'like_status': True
        }
        request = self.factory.post(reverse('like_post'), request_data, content_type='application/json')
        request.user = self.user2
        
        # Submit to like_post view and assert response
        response = views.like_post(request)
        self.assertEqual((response.status_code), (400), response.content)
    

"""
TO DOs
https://docs.djangoproject.com/en/5.0/topics/testing/overview/
https://docs.djangoproject.com/en/5.0/topics/testing/tools/
https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#django.test.RequestFactory
https://docs.djangoproject.com/en/5.0/topics/testing/tools/#liveservertestcase
"""
