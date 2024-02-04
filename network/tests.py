from django.test import Client, TestCase
from django.urls import reverse
from .models import User, Profile, Post

# Create your tests here.
class Create_Profile_Signal_Test(TestCase):

    def testCreateUser(self):
        """Test profile creation upon user creation."""
        self.user = User.objects.create_user(username='testuser1', email='test@example.com', password='12345@Test')
        self.profile = Profile.objects.get(user=self.user)
        self.assertEqual(self.profile.user.username, self.user.username)



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
