from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from .forms import Taskform
from .models import Task

# Create your views here.
def singup (request):
    if request.method == 'GET':
        return render(request,'singup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError:
                return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'User already exist'})
        else:
            return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'Password does not match'})


#login required for these:
@ login_required
def task(request):
    #tasks = get_list_or_404(Task, user=request.user, completed__isnull=True)
    tasks = Task.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'task.html', {'tasks': tasks})


@ login_required
def completed_tasks(request):
    #tasks = get_list_or_404(Task, user=request.user, completed__isnull=False)
    tasks = Task.objects.filter(user=request.user, completed__isnull=False)
    return render(request, 'task.html', {'tasks': tasks})


@ login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': Taskform})
    else:
        try:
            form = Taskform(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        except ValueError:
            return render(request, 'create_task.html', {'form': Taskform, 'error': 'Please provide valid data'})


@ login_required
def task_details(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = Taskform(instance=task)
        if task.user == request.user:
            return render(request, 'task_detail.html', {'task': task, 'form': form})
        else:
            return redirect('task')
    else:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = Taskform(request.POST, instance=task)
        form.save()
        return redirect('task')


@ login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = timezone.now()
        task.save()
        return redirect('task')
    else:
        pass


@ login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')
    else:
        pass

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username= request.POST['username'],
            password= request.POST['password']
        )
        if user is None:
            return render(request, 'login.html', {'error': 'User does not exist, or incorrect Password'})
        else:
            login(request, user)
            return redirect('task')

def log_out(request):
    logout(request)
    return redirect('home')