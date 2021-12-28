from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.blog, name='blog'),
    path('delete/<slug:pk>/', views.delete_blog, name='delete-blog'),
    path('edit/<slug:pk>/', views.edit_blog, name='edit-blog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
