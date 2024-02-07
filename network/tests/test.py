from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from network.models import User, Profile, Post

from network import views

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

    

"""
TO DOs
https://docs.djangoproject.com/en/5.0/topics/testing/overview/
https://docs.djangoproject.com/en/5.0/topics/testing/tools/
https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#django.test.RequestFactory
https://docs.djangoproject.com/en/5.0/topics/testing/tools/#liveservertestcase
"""
