from django.test import Client, TestCase
from django.urls import reverse
from .models import User, Profile, Post

# Create your tests here.
class ViewsTestCase(TestCase):

    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='testuser1', email='test@example.com', password='12345@Test')

    def testLogin(self):
        """Test user login"""
        c = Client()
        response = c.login(username='testuser1', password='12345@Test')
        self.assertEqual(response, True)

"""
TO DOs
https://docs.djangoproject.com/en/5.0/topics/testing/overview/
https://docs.djangoproject.com/en/5.0/topics/testing/tools/
https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#django.test.RequestFactory
https://docs.djangoproject.com/en/5.0/topics/testing/tools/#liveservertestcase

Test all views logged out
Test all views logged in
Test Post submission

"""
