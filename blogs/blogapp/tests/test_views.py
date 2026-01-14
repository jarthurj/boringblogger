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
class PostList(TestCase):
    def test_postlist_loads(self):
         response = self.client.get(reverse("postlist"))
         self.assertEqual(response.status_code,200)

class DeletePost(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",password="assASSass123"
        )
        self.client.login(username="testuser",password="assASSass123")

    def test_delete_requires_login(self):
        self.client.logout()
        p = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        response = self.client.post(
            reverse("delete",args=[p.id])
            )
        self.assertEqual(response.status_code,302)
        redirect_url = "/login/?next=/blogapp/delete/"+str(p.id)+"/"
        self.assertRedirects(
            response,
            redirect_url
        )

    def test_delete(self):
        p = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        p_id = p.id
        p_user = p.author
        response = self.client.post(
            reverse("delete",args=[p_id])
            )
        self.assertEqual(Post.objects.filter(id=p_id).exists(),False)
        self.assertEqual(p_user,self.user)
        
class EditPost(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",password="assASSass123"
        )
        self.client.login(username="testuser",password="assASSass123")

    def test_edit_requires_login(self):
        self.client.logout()
        p = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        response = self.client.post(
            reverse("editpost",args=[p.id])
            )
        self.assertEqual(response.status_code,302)
        redirect_url = "/login/?next=/blogapp/editpost/"+str(p.id)+"/"
        self.assertRedirects(
            response,
            redirect_url
        )
    def test_edit(self):
        p = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        response = self.client.post(
            reverse("editpost",args=[p.id]),
            {
                "title":"THIS IS THE NEW TITLE",
                "content":"NEW CONTENT"
            }
        )
        self.assertEqual(response.status_code,302)
        p.refresh_from_db()
        self.assertEqual(p.title, "THIS IS THE NEW TITLE")
        self.assertEqual(p.content, "NEW CONTENT")
        self.assertEqual(p.author,self.user)