from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm
from .models import Profile

# Home page
def index(request):
    return render(request, 'accountRegistrations/index.html')


# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'accountRegistrations/register.html', context)


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'accountRegistrations/login.html', context)


# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')


# Upload profile picture view
@login_required
def upload_profile_picture(request):
    # ✅ Ensure profile exists for this user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('index')  # redirect wherever you want after upload
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accountRegistrations/profilePic.html', {'form': form})

