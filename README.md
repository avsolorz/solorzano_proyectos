# Gestor de Proyectos de Eventos

**Allison Solórzano**

---

## Descripción

API REST desarrollada con Django REST Framework para la gestión 
de proyectos de eventos. El sistema se basa en la planificación,
coordinación y seguimiento de eventos desde el pedido hasta su
ejecución, permitiendo administrar clientes, asignar coordinadores,
organizar tareas por prioridad, gestionar proveedores de servicios y
controlar publicaciones en redes sociales a través de diseñadores
asignados.

Cuenta con autenticación JWT y un esquema de permisos por roles que
garantiza que cada usuario acceda únicamente a la información que le
corresponde.

---

## Tecnologías

- Python 3.12
- Django 4.x
- Django REST Framework
- PostgreSQL
- JWT — djangorestframework-simplejwt
- uv (gestor de paquetes)
- django-filter
- django-cors-headers

---

## Requisitos previos

- Python 3.12 instalado
- PostgreSQL instalado y corriendo
- uv instalado → `pip install uv`

---

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/avsolorz/solorzano_proyectos.git
cd solorzano_proyecto
```

### 2. Instalar dependencias

```bash
uv sync
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente
contenido:

```env
# Django
SECRET_KEY=django-insecure-solorzano_proyectos-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=solorzano_proyecto_db
DB_USER=solorzano_user
DB_PASSWORD=gestor
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOW_ALL_ORIGINS=True

# Test database
TEST_DB_NAME=solorzano_proyectos_test_db
```

### 4. Crear la base de datos y el usuario en PostgreSQL

```bash
psql -U postgres
```

Dentro de psql ejecuta:

```sql
CREATE DATABASE solorzano_proyecto_db;
CREATE USER solorzano_user WITH PASSWORD 'gestor';
GRANT ALL PRIVILEGES ON DATABASE solorzano_proyecto_db TO solorzano_user;

-- Base de datos para tests
CREATE DATABASE solorzano_proyectos_test_db;
GRANT ALL PRIVILEGES ON DATABASE solorzano_proyectos_test_db TO solorzano_user;
\q
```

### 5. Ejecutar migraciones

```bash
uv run manage.py migrate
```

### 6. Crear superusuario administrador

```bash
uv run manage.py createsuperuser
```

### 7. Correr el servidor

```bash
uv run manage.py runserver
```

El servidor queda disponible en: `http://localhost:8000`

---

## Autenticación

El proyecto usa **JWT (JSON Web Tokens)**. Para acceder a los endpoints
protegidos debes primero obtener un token y luego incluirlo en el header
de cada petición.

### Obtener token

```bash
POST /auth/login/
Content-Type: application/json

{
  "correo": "usuario@ejemplo.com",
  "contraseña": "tu_password"
}
```

Respuesta:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5...",
  "usuario": {
    "id": 1,
    "correo": "usuario@ejemplo.com",
    "nombre": "Allison",
    "rol": "admin"
  }
}
```

### Usar el token

Incluye el token en el header `Authorization` de cada petición:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5...
```

### Renovar token

```bash
POST /auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5..."
}
```

---

## Endpoints

### Sistema

| Método | Ruta       | Descripción         | Auth |
|--------|------------|---------------------|------|
| GET    | `/health/` | Estado del servidor | No   |

### Autenticación

| Método | Ruta                      | Descripción                   | Auth |
|--------|---------------------------|-------------------------------|------|
| POST   | `/auth/login/`            | Iniciar sesión, obtener token | No   |
| POST   | `/auth/refresh/`          | Renovar access token          | No   |
| POST   | `/auth/registro/`         | Registrar nuevo usuario       | No   |
| POST   | `/auth/logout/`           | Cerrar sesión                 | Sí   |
| GET    | `/auth/perfil/`           | Ver perfil del usuario actual | Sí   |
| PATCH  | `/auth/cambiar-password/` | Cambiar contraseña            | Sí   |

### Usuarios

| Método | Ruta               | Descripción        | Auth  |
|--------|--------------------|--------------------|-------|
| GET    | `/usuarios/`       | Listar usuarios    | Admin |
| GET    | `/usuarios/{id}/`  | Detalle de usuario | Admin |
| POST   | `/usuarios/`       | Crear usuario      | Admin |
| PUT    | `/usuarios/{id}/`  | Actualizar usuario | Admin |
| DELETE | `/usuarios/{id}/`  | Eliminar usuario   | Admin |

### Clientes

| Método | Ruta              | Descripción        | Auth        |
|--------|-------------------|--------------------|-------------|
| GET    | `/clientes/`      | Listar clientes    | Autenticado |
| GET    | `/clientes/{id}/` | Detalle de cliente | Autenticado |
| POST   | `/clientes/`      | Crear cliente      | Admin       |
| PUT    | `/clientes/{id}/` | Actualizar cliente | Admin       |
| DELETE | `/clientes/{id}/` | Eliminar cliente   | Admin       |

Filtros disponibles: `?nombre=` `?correo=`

### Eventos

| Método | Ruta                    | Descripción           | Auth        |
|--------|-------------------------|-----------------------|-------------|
| GET    | `/eventos/`             | Listar eventos        | Autenticado |
| GET    | `/eventos/{id}/`        | Detalle de evento     | Autenticado |
| POST   | `/eventos/`             | Crear evento          | Autenticado |
| PUT    | `/eventos/{id}/`        | Actualizar evento     | Autenticado |
| DELETE | `/eventos/{id}/`        | Eliminar evento       | Admin       |
| GET    | `/eventos/{id}/tareas/` | Tareas del evento     | Autenticado |

Filtros disponibles: `?estado=` `?fecha_evento_desde=`
`?fecha_evento_hasta=` `?cliente_nombre=`

### Tareas

| Método | Ruta                           | Descripción      | Auth        |
|--------|--------------------------------|------------------|-------------|
| GET    | `/tareas/`                     | Listar tareas    | Autenticado |
| GET    | `/tareas/{id}/`                | Detalle de tarea | Autenticado |
| POST   | `/tareas/`                     | Crear tarea      | Autenticado |
| PUT    | `/tareas/{id}/`                | Actualizar tarea | Autenticado |
| DELETE | `/tareas/{id}/`                | Eliminar tarea   | Admin       |
| PATCH  | `/tareas/{id}/cambiar-estado/` | Cambiar estado   | Autenticado |

Filtros disponibles: `?estado=` `?prioridad=` `?evento_id=`

### Proveedores

| Método | Ruta                 | Descripción          | Auth        |
|--------|----------------------|----------------------|-------------|
| GET    | `/proveedores/`      | Listar proveedores   | Autenticado |
| GET    | `/proveedores/{id}/` | Detalle de proveedor | Autenticado |
| POST   | `/proveedores/`      | Crear proveedor      | Admin       |
| PUT    | `/proveedores/{id}/` | Actualizar proveedor | Admin       |
| DELETE | `/proveedores/{id}/` | Eliminar proveedor   | Admin       |

Filtros disponibles: `?nombre_empresa=` `?servicio=`

### Redes Sociales

| Método | Ruta                    | Descripción           | Auth        |
|--------|-------------------------|-----------------------|-------------|
| GET    | `/redes-sociales/`      | Listar redes sociales | Autenticado |
| GET    | `/redes-sociales/{id}/` | Detalle de red social | Autenticado |
| POST   | `/redes-sociales/`      | Crear red social      | Admin       |
| PUT    | `/redes-sociales/{id}/` | Actualizar red social | Admin       |
| DELETE | `/redes-sociales/{id}/` | Eliminar red social   | Admin       |

### Diseñadores

| Método | Ruta                 | Descripción          | Auth        |
|--------|----------------------|----------------------|-------------|
| GET    | `/disenadores/`      | Listar diseñadores   | Autenticado |
| GET    | `/disenadores/{id}/` | Detalle de diseñador | Autenticado |
| POST   | `/disenadores/`      | Crear diseñador      | Admin       |
| PUT    | `/disenadores/{id}/` | Actualizar diseñador | Admin       |
| DELETE | `/disenadores/{id}/` | Eliminar diseñador   | Admin       |

Filtros disponibles: `?nombre=` `?especialidad=`

---

## Ejemplos con curl

### Login

```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"correo":"admin@gestor.com","contraseña":"admin123"}'
```

### Crear un evento

```bash
curl -X POST http://localhost:8000/eventos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{
    "nombre_evento": "Conferencia Tech 2025",
    "descripcion": "Evento de tecnología",
    "fecha_evento": "2025-08-15",
    "ubicacion": "Guayaquil, Ecuador",
    "presupuesto": "5000.00",
    "estado": "planificacion",
    "cliente": 1,
    "coordinador": 1
  }'
```

### Listar tareas con filtro

```bash
curl -X GET "http://localhost:8000/tareas/?prioridad=alta&estado=pendiente" \
  -H "Authorization: Bearer <tu_token>"
```

### Cambiar estado de una tarea

```bash
curl -X PATCH http://localhost:8000/tareas/1/cambiar-estado/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token>" \
  -d '{"estado": "completada"}'
```

### Ver mi perfil

```bash
curl -X GET http://localhost:8000/auth/perfil/ \
  -H "Authorization: Bearer <tu_token>"
```

---

## Colección Thunder Client / Postman

El archivo `thunder_collection.json` en la raíz del proyecto contiene
todos los endpoints listos para importar.

Para importar en Thunder Client:
1. Abre Thunder Client en VS Code
2. Click en `Collections` → `Import`
3. Selecciona el archivo `thunder_collection.json`

Para importar en Postman:
1. Click en `Import`
2. Selecciona el archivo `thunder_collection.json`

---

## Despliegue

URL de producción: `solorzano-proyectos.uaeftt-ute.site]`


---

## Roles del sistema

| Rol         | Descripción                                  |
|-------------|----------------------------------------------|
| admin       | Acceso total — crear, editar y eliminar todo |
| coordinador | Gestiona sus propios eventos y tareas        |
| asistente   | Solo lectura                                 |