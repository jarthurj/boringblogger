from django.contrib import admin
from django.urls import path,include
from . import views
from blogapp.views import Dashboard,NewPost
urlpatterns = [
    # path('dashboard/',views.dashboard, name="dashboard"),
    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    # path('newpost/',views.newpost,name="newpost"),
    path('newpost/',NewPost.as_view(),name="newpost"),
    path('delete/<int:pk>',views.deletepost,name="delete"),
    # path('home/',views.home,name="home"),
    path('postlist/',views.postlist,name="postlist"),
    path('editpost/<int:pk>',views.editpost,name="editpost")
]
