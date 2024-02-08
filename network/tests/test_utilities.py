import json

from django.test import TestCase

from network.utilities import check_json
from network.models import User, Profile, Post

# Create your tests here.

class check_json_test(TestCase):
    def setUp(self) -> None:
        # Create test User, Post and Profile
        new_user = User.objects.create_user(username='testuser', email='test@example.com', password='12345@Test') 
        self.profile = Profile.objects.get(user=new_user)
        new_post = Post(owner=self.profile, text="Test post.")
        new_post.save()
        self.post = Post.objects.filter(owner=self.profile).first()

    def test_like(self):
        """Test valid data for liking a post"""
        data = json.dumps({
            'id': self.post.id,
            'action': 'like',
            'modifier': True
        })

        clean_data, message = check_json(data)
        self.assertEqual((clean_data['target'], clean_data['modifier']), (self.post, True))

    def test_like_modifier(self):
        """Test missing modifier for liking a post"""
        data = json.dumps({
            'id': self.post.id,
            'action': 'like',
            'modifier': None
        })

        clean_data, message = check_json(data)
        self.assertEqual(clean_data, None)

    def test_follow(self):
        """Test valid data for following a profile"""
        data = json.dumps({
            'id': self.profile.id,
            'action': 'follow',
            'modifier': False
        })

        clean_data, message = check_json(data)
        self.assertEqual((clean_data['target'], clean_data['modifier']), (self.profile, False))

    def test_follow_modifier(self):
        """Test missing modifier for following a profile"""
        data = json.dumps({
            'id': self.profile.id,
            'action': 'follow',
            'modifier': None,
        })

        clean_data, message = check_json(data)
        self.assertEqual(clean_data, None)

    def test_edit(self):
        """Test valid data for editing a post"""
        data = json.dumps({
            'id': self.post.id,
            'action': 'edit',
            'text': 'new edits'
        })

        clean_data, message = check_json(data)
        self.assertEqual((clean_data['target'], clean_data['text']), (self.post, 'new edits'))

    def test_edit_content(self):
        """Test missing content for editing a post"""
        data = json.dumps({
            'id': self.post.id,
            'action': 'edit',
            'text': None
        })

        clean_data, message = check_json(data)
        self.assertEqual(clean_data, None)

    def test_invalid_id(self):
        # Get pk of last post item
        last_post = Post.objects.order_by('pk').last()

        data = json.dumps({
            'id': last_post.id + 1,
            'action': 'edit',
            'text': 'new edits'
        })

        clean_data, message = check_json(data)
        self.assertEqual((clean_data, message), (None, f'ID: {last_post.id + 1} not found'))
        