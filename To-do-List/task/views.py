from django.conf.urls import url
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import CreateTaskForm, CreateUserForm

# Create your views here.


@login_required(login_url='login_user')
def todo_list(request):
    if request.user.is_authenticated:
        user = request.user
        task = user.task_set.all()  # or task = Task.objects.filter(user=user)
        context = {'task': task}
        return render(request, 'task/to_do_list.html', context)
    # else:
    #     task = Task.objects.filter(user__exact=None)
    #     context = {'task': task}
    #     return render(request, 'task/to_do_list.html', context)


@login_required(login_url='login_user')
def todo_detail(request, pk):
    # if request.user
    user = request.user.task_set
    task = get_object_or_404(user, pk=pk)
    context = {'task': task}
    return render(request, 'task/to_do_detail.html', context)


@login_required(login_url='login_user')
def todo_create(request):
    if request.user.is_authenticated:
        user = request.user
        form = CreateTaskForm()
        if request.method == 'POST':
            form = CreateTaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = user
                task.save()
                messages.success(request, "Task successfully created")
                return redirect('todo_list')
            else:
                messages.error(request, "Please fill the form carefully")
        context = {'form': form}
        return render(request, 'task/to_do_create.html', context)


@login_required(login_url='login_user')
def todo_update(request, pk):
    user = request.user.task_set
    task = get_object_or_404(user, pk=pk)
    form = CreateTaskForm(instance=task)
    # task = get_object_or_404(Task, pk=pk)
    #  or if request.user == task.user
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task successfully updated")
            return redirect('todo_detail', pk=pk)
        else:
            messages.error(request, "Please fill the form carefully")

    context = {'form': form}
    return render(request, 'task/to_do_create.html', context)


@login_required(login_url='login_user')
def todo_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task successfully deleted")
    return redirect('todo_list')


###################################################################################################################
############## User Registration ##################################################################################


def register_user(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account successfully created")
                return redirect('login_user')
            else:
                messages.error(request, "Please fill the form carefully")

        context = {'form': form}
        return render(request, 'user_register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # if user is not None:if user.is_active: login(request, user) ...
        if user:
            login(request, user)
            return redirect('todo_list',)
        else:
            messages.error(request, "username or password is incorrect")
    context = {}
    return render(request, 'user_login.html', context)


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('todo_list')
