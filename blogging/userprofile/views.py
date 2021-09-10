from userprofile.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import UserCreateForm, ProfileForm

# Create your views here.


def create_user(request):
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully Registered')
            return redirect('login')
        else:
            messages.error(request, 'Please fill all the field carefully')

    context = {'form': form}
    return render(request, 'userprofile/register.html', context)


@login_required(login_url='login')
def user_profile(request, pk):
    # or we can get the profile id from templates request.user.profile.id
    profile = get_object_or_404(Profile, pk=pk)
    context = {'profile': profile}
    return render(request, 'userprofile/profile.html', context)


@login_required(login_url='login')
def user_account(request):
    # or we can get the profile id from templates request.user.profile.id
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'userprofile/profile.html', context)


@login_required(login_url='login')
def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile edited successfully')
            return redirect('user_profile', pk=pk)
        else:
            messages.error(request, 'please fill all the field carefully')
    context = {'form': form}
    return render(request, 'userprofile/profile_form.html', context)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't does not exist")
        else:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'logged in Successfully')
                return redirect('index')
            else:
                messages.error(request, "username or password didn't match")
    return render(request, 'userprofile/login.html')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request, 'logged out Successfully')
    return redirect('login')
