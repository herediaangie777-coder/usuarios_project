# Centro de Entrenamiento E-Sports

Sistema de información para gestionar el Centro de Entrenamiento de E-Sports de Ciudad del Río. El proyecto incluye un backend con Django y Django REST Framework, un frontend vanilla que consume la API pública y documentación técnica para despliegue local.

## Stack tecnológico

- Python 3.10+
- Django 4.2+
- Django REST Framework 3.14+
- SQL Server 2019+ o MySQL 8+
- python-dotenv
- CoreAPI para documentación
- HTML, CSS y JavaScript vanilla para el frontend

## Estructura

- [backend/](./backend): proyecto Django
- [frontend/](./frontend): frontend vanilla consumiendo la API pública
- [database/schema.sql](./database/schema.sql): script DDL
- [database/seed.sql](./database/seed.sql): datos de prueba
- [docs/](./docs): diagramas y documentación de apoyo
- [.env.example](./.env.example): plantilla de variables de entorno

## Prerrequisitos

- Python 3.10 o superior
- SQL Server 2019+ con ODBC Driver 17 o MySQL 8+
- Git
- UV recomendado o PIP como alternativa

## Instalación con UV

```bash
uv venv
uv pip install -r requirements.txt
```

## Instalación con PIP

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración `.env`

1. Copia `.env.example` como `.env`.
2. Ajusta las credenciales según tu motor de base de datos.

Ejemplo para SQL Server:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=mssql
DB_NAME=proyecto_sena
DB_USER=
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=1433
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_EXTRA_PARAMS=Trusted_Connection=yes;Encrypt=no
```

Ejemplo para MySQL:

```env
DB_ENGINE=mysql
DB_NAME=proyecto_sena
DB_USER=root
DB_PASSWORD=secret
DB_HOST=127.0.0.1
DB_PORT=3306
DB_CHARSET=utf8mb4
```

## Base de datos

Puedes trabajar de dos formas:

### Opción 1. Migraciones Django

```bash
cd backend
py manage.py makemigrations
py manage.py migrate
```

### Opción 2. Script SQL

Ejecuta:

- [database/schema.sql](./database/schema.sql)
- [database/seed.sql](./database/seed.sql)

## Superusuario y servidor

```bash
cd backend
py manage.py createsuperuser
py manage.py runserver
```

## URLs principales

- API pública: `http://localhost:8000/api/v1/`
- Documentación: `http://localhost:8000/docs/`
- Admin: `http://localhost:8000/admin/`
- Front interno basado en templates: `http://localhost:8000/`

## Endpoints públicos

- `GET|POST|PUT|PATCH|DELETE /api/v1/plataformas/`
- `GET|POST|PUT|PATCH|DELETE /api/v1/juegos/`
- `GET|POST|PUT|PATCH|DELETE /api/v1/equipos/`

La lógica de usuarios, sesiones, trofeos y hardware permanece implementada en el backend y administrable desde Django Admin.

## Ejecutar el frontend

El frontend se encuentra en [frontend/index.html](./frontend/index.html) y consume `http://localhost:8000/api/v1/`.

Puedes abrirlo con cualquier servidor estático simple. Ejemplo con Python:

```bash
cd frontend
py -m http.server 5500
```

Luego abre:

- `http://localhost:5500`

## Diagramas

- [docs/diagrama_clases.pdf](./docs/diagrama_clases.pdf)
- [docs/diagrama_relacional.pdf](./docs/diagrama_relacional.pdf)
- [docs/diagrama_clases_centro_entrenamiento_v4_final.html](./docs/diagrama_clases_centro_entrenamiento_v4_final.html)

## Notas

- `.env` está ignorado en `.gitignore`.
- El backend sigue el patrón split-folder en `api/models`, `api/serializers` y `api/views`.
- El frontend implementa manejo básico de errores HTTP y de red.
