from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def home(request):
    return render(request, 'home.html')


def registrarse(request):
    if request.method == 'GET':
        return render(request, 'registrarse.html',
                      {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'registrarse.html',
                      {'form': UserCreationForm,
                       "error": 'Usuario ya existe'}
                      )
        else:
            return render(request, 'registrarse.html',
                      {'form': UserCreationForm,
                       "error":'Password no coinciden'}
                       )
            
def tasks(request):
    return render(request, 'tasks.html')

def cerrar_session(request):
    logout(request)
    return redirect('home')

def iniciar_session(request):
    if request.method == 'GET':
        return render(request, 'iniciar_session.html',
                      {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'iniciar_session.html',
                          {'form': AuthenticationForm,
                           "error": 'Usuario o password es incorrecto'})
        else:
            login(request, user)
            return redirect('tasks')

def crear_tarea(request):
    return render(request, 'crear_tarea.html')