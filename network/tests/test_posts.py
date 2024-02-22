import json

from django.test import TestCase, RequestFactory
from django.urls import reverse
from network.models import User, Profile, Post

from network import views

class GET_posts_test(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        # Create User
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='12345@Test')
        profile1 = Profile.objects.get(user=self.user1)        
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='12345@Test')
        profile2 = Profile.objects.get(user=self.user2)

        # Create test posts
        for i in range(15):
            new_post = Post(owner=profile1, text=f"Test post {i + 1}.")
            new_post.save()

        for i in range(15):
            new_post = Post(owner=profile2, text=f"Test post {i + 1}.")
            new_post.save()

    def test_show_all(self):
        """Test getting all posts page 1"""

        # Create request
        page = 1
        url = f"{reverse('posts', kwargs = {'category': 'all'})}?page={page}"
        request = self.factory.get(url)

        response = views.posts(request)
        response_data = json.loads(response.content)

        # Response status should be 200
        self.assertEqual(response.status_code, 200)

        # JSON content should have test posts 15 to 6
        self.assertEqual(10, len(response_data))
        self.assertEqual('Test post 15.', response_data[0]['text'])


