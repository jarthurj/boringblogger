from django.contrib import admin
from django.urls import path,include
from . import views
from blogapp.views import Dashboard,NewPost,PostList,DeletePost,EditPost,NewComment
urlpatterns = [
    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    path('newpost/',NewPost.as_view(),name="newpost"),
    path('delete/<int:pk>/',DeletePost.as_view(),name="delete"),
    path('editpost/<int:pk>/',EditPost.as_view(),name='editpost'),
    path('postlist/',PostList.as_view(),name="postlist"),
    path('comment/<int:pk>/',NewComment.as_view(),name='newcomment'),
]
