from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin panel
    path('', include('photogallery_project_app.urls')),  # Include our app's routes
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ Built-in auth
]
