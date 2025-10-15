from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task

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

    tareas= Task.objects.filter(user=request.user, fecha_completado__isnull=True)
    return render(request, 'tasks.html', {'tareas': tareas})

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
    if request.method == 'GET':
        return render(request, 'crear_tarea.html',{'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')

        except ValueError:
            return render(request, 'crear_tarea.html',{
                'form': TaskForm,
                'error': 'Por favor ingresa datos validos'})

def detalle_tarea(request, tarea_id):#Permite mostar el titulo de una tarea
    if request.method == 'GET':
        # tarea=Task.objects.get(pk=tarea_id)  #solo muestra las tarea que tiene id si no esta tumba servidor
        tarea = get_object_or_404(Task, pk=tarea_id) #si no existe tarea id solo muestra 404, no cae servidor
        form=TaskForm(instance=tarea)
        return render(request, 'detalle_tarea.html', {'tarea':tarea, 'form': form})
    else:
        try:
            tarea = get_object_or_404(Task, pk=tarea_id) #buscar en  Task la pk que coincida con tarea_id, si la obtiene guardar en tarea
            form = TaskForm(request.POST, instance=tarea) #TaskForm va recibir todos los datos que vienen en POST y va decir que es una instancia de Task. Genera un nuevo form
            form.save()# el nuevo formulario se guarda
            return redirect('tasks')
        except ValueError:
            tarea = get_object_or_404(Task, pk=tarea_id)
            form = TaskForm(instance=tarea)
            return render(request, 'detalle_tarea.html', {
                'tarea':tarea,
                'form': form,
                'error': "Error al actualizar tarea"})
