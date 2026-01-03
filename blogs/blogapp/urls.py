from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard, name="dashboard"),
    path('newpost/',views.newpost,name="newpost"),
    path('delete/<int:pk>',views.deletepost,name="delete"),
    # path('home/',views.home,name="home"),
    path('postlist/',views.postlist,name="postlist")
]
