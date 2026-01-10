from django.test import TestCase
from blogapp.models import Post
from django.contrib.auth.models import User
class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",password="assASSass123"
        )
    def test_post_creation(self):
        post = Post.objects.create(
            title = "Test Post",
            content = "Hello Buttrss",
            author = self.user,
        )
        self.assertEqual(post.title,"Test Post")

