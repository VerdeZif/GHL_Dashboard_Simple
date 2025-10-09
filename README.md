# GHL Dashboard Simple

Dashboard simple de métricas y reporting para GoHighLevel (GHL).

## 📋 Descripción

GHL Dashboard Simple es una aplicación web desarrollada en Django que proporciona visualización de métricas y reportes para sistemas GoHighLevel. El proyecto incluye funcionalidades para gestión de citas, calendarios y generación de reportes personalizados.

## 🚀 Características

- **Dashboard de Métricas**: Visualización centralizada de KPIs y métricas importantes
- **Gestión de Citas**: Módulo completo para administrar appointments
- **Calendario GHL**: Integración con calendarios de GoHighLevel
- **Sistema de Reportes**: Generación de reportes estáticos con visualizaciones
- **API REST**: Endpoints para integración con servicios externos
- **Testing Integrado**: Suite completa de pruebas automatizadas

## 📁 Estructura del Proyecto

```
GHL_DASHBOARD_SIMPLE/
├── appointments/           # Módulo de gestión de citas
│   ├── migrations/        # Migraciones de base de datos
│   ├── tests/            # Tests del módulo
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Vistas y controladores
│   ├── urls.py           # Rutas del módulo
│   └── serializers.py    # Serializadores para API
│
├── ghl_calendar/          # Módulo de calendario GHL
│   ├── asgi.py           # Configuración ASGI
│   ├── settings.py       # Configuración del proyecto
│   ├── urls.py           # Rutas principales
│   └── wsgi.py           # Configuración WSGI
│
└── reports/              # Módulo de reportes
    ├── static/
    │   └── reports/
    │       ├── css/      # Estilos personalizados
    │       └── js/       # Scripts JavaScript
    ├── templates/
    │   └── reports/
    │       └── dashboard.html
    └── tests/            # Tests del módulo de reportes
```

## 🛠️ Tecnologías

- **Backend**: Django 4.x
- **Base de Datos**: Compatible con PostgreSQL/MySQL/SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **API**: Django REST Framework
- **Testing**: Python unittest

## 📦 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip
- virtualenv (recomendado)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/VerdeZif/GHL_Dashboard_Simple.git
cd GHL_Dashboard_Simple
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Iniciar servidor de desarrollo**
```bash
python manage.py runserver
```

La aplicación estará disponible en `http://localhost:8000`

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/ghl_dashboard

# GoHighLevel API
GHL_API_KEY=tu-api-key
GHL_API_URL=https://api.gohighlevel.com
```

## 🧪 Testing

Ejecutar todos los tests:
```bash
python manage.py test
```

Ejecutar tests de un módulo específico:
```bash
python manage.py test appointments
python manage.py test reports
```

Con cobertura:
```bash
coverage run manage.py test
coverage report
```

## 📊 Módulos

### Appointments
Gestión completa de citas incluyendo:
- Creación y edición de appointments
- Visualización de calendario
- Integración con GHL API
- Serialización de datos

### Reports
Sistema de reportes con:
- Dashboard principal con métricas
- Gráficos y visualizaciones
- Reportes estáticos exportables
- Plantillas personalizables

### GHL Calendar
Sincronización con calendarios de GoHighLevel:
- Importación de eventos
- Actualización en tiempo real
- Gestión de disponibilidad

## 🚀 Despliegue

### Producción con Gunicorn

```bash
gunicorn ghl_calendar.wsgi:application --bind 0.0.0.0:8000
```

### Con Docker

```bash
docker build -t ghl-dashboard .
docker run -p 8000:8000 ghl-dashboard
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

**VerdeZif , Jaime-D-Z**
- GitHub: [@VerdeZif](https://github.com/VerdeZif)

- GitHub: [@Jaime-D-Z](https://github.com/Jaime-D-Z)


## 📧 Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio de GitHub.

## 🙏 Agradecimientos

- Equipo de GoHighLevel por su API
- Comunidad de Django por el excelente framework
- Todos los contribuidores del proyecto

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
