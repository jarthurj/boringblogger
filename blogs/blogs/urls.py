
from django.contrib import admin
from django.urls import path,include
from blogs import urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blogapp.urls')),
]
