from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),  # ✅ Like/unlike
    path('upload/', views.upload_photo, name='upload_photo'),
    path('register/', views.register, name='register'),  # For user sign-up
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # For user login
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),  # For user logout
]
