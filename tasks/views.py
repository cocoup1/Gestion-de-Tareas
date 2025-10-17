from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone

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

@login_required            
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

@login_required
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

@login_required
def detalle_tarea(request, tarea_id):#Permite mostar el titulo de una tarea
    if request.method == 'GET':
        # tarea=Task.objects.get(pk=tarea_id)  #solo muestra las tarea que tiene id si no esta tumba servidor
        #Obtener solo su tarea o las tareas de un solo usuario
        tarea = get_object_or_404(Task, pk=tarea_id, user=request.user) #si no existe tarea id solo muestra 404, no cae servidor
        form=TaskForm(instance=tarea)
        return render(request, 'detalle_tarea.html', {'tarea':tarea, 'form': form})
    else:
        try:
            #obtener la tarea solo del usuario
            tarea = get_object_or_404(Task, pk=tarea_id, user=request.user) #buscar en  Task la pk que coincida con tarea_id, el user con el request.user y si la obtiene guardar en tarea
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

@login_required
def tarea_completa (request, tarea_id):
    tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
    if request.method == "POST":
        tarea.fecha_completado = timezone.now()
        tarea.save()
        return redirect ('/tasks/')

@login_required
def listar_tarea_completada(request):

    tareas= Task.objects.filter(user=request.user, fecha_completado__isnull=False).order_by('-fecha_completado')
    return render(request, 'tasks.html', {'tareas': tareas})

@login_required
def eliminar_tarea (request, tarea_id):
    tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
    if request.method == "POST":
        tarea.delete()
        return redirect ('/tasks/')