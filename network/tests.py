from django.test import TestCase
from .models import User, Profile, Post

# Create your tests here.
class PostTestCase(TestCase):

    def setUp(self):
        # Create test users
        user1 = User.objects.create_user(username='testuser1', password='12345@Test')
        u1 = Profile.objects.create(user=user1)
        user2 = User.objects.create_user(username='testuser2', password='12345@Test')
        u2 = Profile.objects.create(user=user2)

        # Create test posts
        Post.objects.create(
            owner=u1,
            text='test post under testuser1',
            )

    def test_add_post(self):
        """Check for post"""
        queried_post = Post.objects.first()

        self.assertEqual(queried_post.text, 'test post under testuser1')


