from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Photo
from .forms import PhotoForm


def home(request):
    """
    Homepage: shows all photos or filters by ?tag=...
    """
    current_tag = request.GET.get('tag')  # e.g. /?tag=Travel

    if current_tag:
        # Simple, practical filter: case-insensitive contains.
        # (Because tags are stored comma-separated; we'll keep it simple.)
        photos = Photo.objects.filter(tags__icontains=current_tag).order_by('-date_uploaded')
    else:
        photos = Photo.objects.all().order_by('-date_uploaded')

    context = {
        'photos': photos,
        'current_tag': current_tag,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def upload_photo(request):
    """
    Upload a new photo. Requires login.
    """
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user  # ensure uploader saved
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'upload_photo.html', {'form': form})


def photo_detail(request, photo_id):
    """
    Single photo page.
    """
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_detail.html', {'photo': photo})


@login_required
def toggle_like(request, photo_id):
    """
    Like/unlike a photo, then bounce back to where the user came from.
    """
    photo = get_object_or_404(Photo, id=photo_id)

    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)

    # Prefer 'next' param, else back to detail, else home.
    next_url = request.GET.get('next')
    if next_url:
        return HttpResponseRedirect(next_url)
    return redirect('photo_detail', photo_id=photo.id)
