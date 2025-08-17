from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),

    # Photos
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/like/', views.toggle_like, name='toggle_like'),

    # Upload
    path('upload/', views.upload_photo, name='upload_photo'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
