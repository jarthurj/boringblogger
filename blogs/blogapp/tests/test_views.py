from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blogapp.models import Post

class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",password="assASSass123"
        )
        self.client.login(username="testuser",password="assASSass123")

    def test_dashboard_loads(self):
        Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogapp/postlist.html")

    def test_dashboard_requires_login(self):
            self.client.logout()
            response = self.client.get(reverse("dashboard"))
            self.assertEqual(response.status_code,302)
            self.assertRedirects(
                response,
                "/login/?next=/blogapp/dashboard/"
            )

class NewPostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",password="assASSass123"
        )
        self.client.login(username="testuser",password="assASSass123")

    def test_newpost_loads(self):
         response = self.client.get(reverse("newpost"))
         self.assertEqual(response.status_code,200)
    def test_newpost_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("newpost"))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(
            response,
            "/login/?next=/blogapp/newpost/"
        )
    def test_create_post(self):
        response = self.client.post(
            reverse("newpost"),
            {
                "title":"NewPost",
                "content":"Post Content"
            }
        )
        self.assertEqual(response.status_code,302)
        self.assertTrue(Post.objects.filter(title="NewPost").exists())
# class CreateViewTest(TestCase):
