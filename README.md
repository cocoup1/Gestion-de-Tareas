Sistema Gestión de Tareas - Django CRUD

Una aplicación web moderna para la gestión personal de tareas desarrollada con Django y Bootstrap. Permite a los usuarios registrarse, autenticarse y gestionar sus tareas de manera individual y segura.

 Características Principales

- Sistema de autenticación completo: Registro, inicio de sesión y cierre de sesión
- CRUD de tareas: Crear, leer, actualizar y eliminar tareas
- Gestión de usuarios: Cada usuario ve solo sus propias tareas
- Interfaz responsiva: Diseño moderno con Bootstrap 5
- Tareas importantes: Marcado especial para tareas prioritarias
- Estado de completado: Seguimiento de tareas pendientes y completadas
- Fecha de creación: Registro automático de cuándo se creó cada tarea


Requisitos

- Python 3.13.6
- Django 5.2.7
- SQLite 
- Bootstrap 5.3


 Clonar el repositorio

git clone https://github.com/cocoup1/Gestion-de-Tareas


Crear entorno virtual

python -m venv venv

Windows
venv\Scripts\activate


Instalar dependencias
pip install -r requirements.txt


Configurar base de datos
python manage.py makemigrations
python manage.py migrate

Crear superusuario (opcional)
python manage.py createsuperuser

Ejecutar servidor de desarrollo
python manage.py runserver

La aplicación estará disponible en `http://127.0.0.1:8000/`

 Uso de la Aplicación

Para nuevos usuarios:
1. Registro: Visita `/registrarse/` para crear una cuenta
2. Inicio de sesión: Accede con tus credenciales en `/iniciar_session/`

Gestión de tareas:
1. Ver tareas: Navega a "Tareas Pendientes" para ver tu lista
2. Crear tarea: Haz clic en "Crear Tarea" y completa el formulario
3. Editar tarea: Haz clic en cualquier tarea para modificarla
4. Marcar como completada: Usa el botón de completar en cada tarea
5. Eliminar tarea: Borra tareas que ya no necesites

 Características especiales:
- Tareas importantes: Marca la casilla "Important" para destacar tareas prioritarias
- Tareas completadas: Ve tu historial en "Tareas Completadas"
- Información de usuario: Cada tarea muestra quién la creó y cuándo

Estructura del Proyecto

ProyectoCrud/
├── djangocrud/          # Configuración principal
│   ├── settings.py      # Configuraciones del proyecto
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Configuración WSGI
├── tasks/               # Aplicación de tareas
│   ├── models.py        # Modelo Task
│   ├── views.py         # Lógica de negocio
│   ├── forms.py         # Formularios
│   └── templates/       # Plantillas HTML
├── requirements.txt     # Dependencias del proyecto
└── manage.py           # Comando principal de Django

Modelo de Datos

  Task (Tarea)
- `titulo`: Título de la tarea (máx. 100 caracteres)
- `descripcion`: Descripción detallada (opcional)
- `created`: Fecha y hora de creación (automática)
- `fecha_completado`: Fecha de completado (opcional)
- `important`: Marca si es tarea importante (booleano)
- `user`: Usuario propietario (relación con User de Django)

Tecnologías Utilizadas

  Backend
- Django 5.2.7: Framework web de Python
- SQLite: Base de datos para desarrollo
- PostgreSQL: Base de datos para producción
- Django Forms: Manejo de formularios y validación

 Frontend
- HTML5: Estructura de páginas
- CSS3: Estilos personalizados
- Bootstrap 5.3.8: Framework CSS responsivo
- Django Templates: Sistema de plantillas


 Seguridad
- Protección CSRF: en todos los formularios
- Autenticación requerida: para acceder a tareas
- Autorización por usuario:  solo ves tus propias tareas
- Validación de formularios: en frontend y backend
- Gestión segura de sesiones


