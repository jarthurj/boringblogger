from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard, name="dashboard"),
    path('newpost/',views.newpost,name="newpost"),
    path('post/<int:pk>',views.viewpost,name="viewpost"),
    path('home',views.home,name="home")
]
