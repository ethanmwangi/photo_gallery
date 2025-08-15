from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Photo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Optional description
    image = models.ImageField(upload_to='photos/')
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    likes = models.ManyToManyField(User, related_name='liked_photos', blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Who uploaded it
    date_uploaded = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return self.title

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',')]
