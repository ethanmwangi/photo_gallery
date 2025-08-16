from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Photo
from .forms import PhotoForm   # ✅ make sure you have forms.py with PhotoForm defined


# Homepage – show all photos
def home(request):
    photos = Photo.objects.all().order_by('-date_uploaded')  # newest first
    return render(request, 'home.html', {'photos': photos})


# User registration
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


# Upload photo (requires login)
@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user  # ✅ attach uploader
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'upload_photo.html', {'form': form})


# Photo detail page
def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_detail.html', {'photo': photo})


# Like/unlike a photo
@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.user in photo.likes.all():
        photo.likes.remove(request.user)  # Unlike
    else:
        photo.likes.add(request.user)  # Like

    return redirect('photo_detail', photo_id=photo.id)
