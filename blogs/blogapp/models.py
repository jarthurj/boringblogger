from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    title = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag,related_name="posts")

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

