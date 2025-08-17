from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')


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
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

