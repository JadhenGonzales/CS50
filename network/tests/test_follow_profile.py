from django.test import TestCase, RequestFactory
from django.urls import reverse
from network.models import User, Profile

from network import views

# Create your tests here.

class Follow_Profile_Test(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create User
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='12345@Test')    
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='12345@Test')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)

        # Create request data
        self.data = {
            'profile_id': self.profile1.id,
            'follow_status': True
        }

    def test_follow_profile(self):
        """Test following a profile."""

        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request = self.factory.post(reverse('follow_profile'), self.data, content_type='application/json')
        request.user = self.user2
        
        # Submit to follow_profile view and assert response
        response = views.follow_profile(request)
        self.assertEqual(response.status_code, 200, response.content)

        # Check if follow saved in database
        target_profile = Profile.objects.get(pk=self.profile1.id)
        self.assertEqual(target_profile.followers.count(), 1)

    def test_like_own(self):
        """Test following your own profile."""

        # Create request
        self.client.login(username='testuser1', password='12345@Test')
        request = self.factory.post(reverse('follow_profile'), self.data, content_type='application/json')
        request.user = self.user1
        
        # Submit to follow_profile view and assert response
        response = views.follow_profile(request)
        self.assertEqual(response.status_code, 400, response.content)

        # Check if follow not saved in database
        target_profile = Profile.objects.get(pk=self.profile1.id)
        self.assertEqual(target_profile.followers.count(), 0)
      
    def test_unlike(self):
        """Test unfollowing an already liked profile."""
        # Initialize already liked state
        self.profile1.followers.add(self.profile2)
        self.profile1.save()

        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request_data = {
            **self.data,
            'follow_status': False
        }
        request = self.factory.post(reverse('follow_profile'), request_data, content_type='application/json')
        request.user = self.user2
        
        # Submit to follow_profile view and assert response
        response = views.follow_profile(request)
        self.assertEqual(response.status_code, 200, response.content)

        # Check if follow saved in database
        target_profile = Profile.objects.get(pk=self.profile1.id)
        self.assertEqual(target_profile.followers.count(), 0)

    def test_submit_invalid(self):
        """Test submitting an invalid JSON"""

        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request_data = {
            'foo':'bar',
            'baz': True
        }
        request = self.factory.post(reverse('follow_profile'), request_data, content_type='application/json')
        request.user = self.user2
        
        # Submit to follow_profile view and assert response
        response = views.follow_profile(request)
        self.assertEqual(response.status_code, 400, response.content)

    def test_like_invalid(self):
        """Test liking an invalid profile id."""
        
        # Get ID of last profile
        last_profile = Profile.objects.order_by('pk').last()
        
        # Create request
        self.client.login(username='testuser2', password='12345@Test')
        request_data = {
            **self.data,
            'profile_id': last_profile.id + 1,
        }
        request = self.factory.post(reverse('follow_profile'), request_data, content_type='application/json')
        request.user = self.user2
        
        # Submit to follow_profile view and assert response
        response = views.follow_profile(request)
        self.assertEqual(response.status_code, 400, response.content)

 