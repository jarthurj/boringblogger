from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blogapp.models import Post,Comment
from django.conf import settings

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
        self.assertContains(response, "Test")
        self.assertEqual(len(response.context["object_list"]),1)

    def test_dashboard_requires_login(self):
            self.client.logout()
            response = self.client.get(reverse("dashboard"))
            self.assertEqual(response.status_code,302)
            self.assertRedirects(
                response,
                f"/{settings.LOGIN_URL}/?next={reverse('dashboard')}"
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
        self.assertTemplateUsed(response,"blogapp/newpost.html")

    def test_newpost_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("newpost"))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(
            response,
            f"/{settings.LOGIN_URL}/?next={reverse('newpost')}"
        )

    def test_create_post(self):
        response = self.client.post(
            reverse("newpost"),
            {
                "title":"NewPost",
                "content":"Post Content",
            }
        )
        self.assertEqual(response.status_code,302)
        post = Post.objects.filter(title="NewPost").first()
        self.assertTrue(post)
        self.assertEqual(self.user,post.author)

class PostList(TestCase):
    def test_postlist_loads(self):
         response = self.client.get(reverse("postlist"))
         self.assertEqual(response.status_code,200)
         self.assertTemplateUsed(response,"blogapp/postlist.html")

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
        self.assertEqual(response.status_code,403)
        # self.assertRedirects(
        #     response,
        #     f"/{settings.LOGIN_URL}/?next={reverse('delete',args=[p.id])}"
        # )
        self.assertTrue(Post.objects.filter(id=p.id).exists())

    def test_delete(self):
        p = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        p_id = p.id
        response = self.client.post(
            reverse("delete",args=[p_id])
            )
        self.assertEqual(Post.objects.filter(id=p_id).exists(),False)

    def test_user_cant_delete_others_post(self):
        other_user = User.objects.create_user(
            username="other", password="pass123"
        )

        post = Post.objects.create(
            title="Test",
            content="Content",
            author=other_user
        )

        response = self.client.post(
            reverse("delete", args=[post.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Post.objects.filter(id=post.id).exists())
 
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

    def test_edit_loads(self):
        p = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        response = self.client.get(reverse("editpost",args=[p.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogapp/newpost.html")

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

class NewComment(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",password="assASSass123"
        )
        self.post = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        self.client.login(username="testuser",password="assASSass123")
    def test_new_comment_loads(self):
        response = self.client.get(reverse("newcomment",args=[self.post.id]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"blogapp/newcomment.html")
    def test_comment_posts(self):
        c = Comment.objects.create(
            content = "CONTENT",
            author = self.user,
            post = self.post
        )
        self.assertTrue(Comment.objects.filter(id=c.id).exists())

    def test_comment_requires_login(self):
        self.client.logout()
        response = self.client.post(reverse('newcomment',args=[self.post.id]),
                                    {
                                        "content":"BUTTS",
                                        "author":self.user,
                                    })
        self.assertEqual(response.status_code,302)
        self.assertIsNone(Comment.objects.all().first())


