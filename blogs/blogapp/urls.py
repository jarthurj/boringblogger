from django.contrib import admin
from django.urls import path,include
from . import views
from blogapp.views import Dashboard,NewPost,PostList,DeletePost,EditPost
urlpatterns = [
    # path('dashboard/',views.dashboard, name="dashboard"),
    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    # path('newpost/',views.newpost,name="newpost"),
    path('newpost/',NewPost.as_view(),name="newpost"),
    # path('delete/<int:pk>',views.deletepost,name="delete"),
    path('delete/<int:pk>/',DeletePost.as_view(),name="delete"),
    path('editpost/<int:pk>/',EditPost.as_view(),name='editpost'),
    # path('home/',views.home,name="home"),
    # path('postlist/',views.postlist,name="postlist"),
    path('postlist/',PostList.as_view(),name="postlist"),
    # path('editpost/<int:pk>',views.editpost,name="editpost")
]
