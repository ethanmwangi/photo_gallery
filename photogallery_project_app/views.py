from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
    photos = Photo.objects.all().order_by('-date_uploaded')  # newest first
    return render(request, 'home.html', {'photos': photos})


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

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # go back to homepage after upload
    else:
        form = PhotoForm()
    return render(request, 'upload_photo.html', {'form': form})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'upload_photo.html', {'form': form})

# Create your views here.
