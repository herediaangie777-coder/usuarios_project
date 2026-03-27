🚀 🧾 MANUAL DEL PROYECTO – USUARIOS PROJECT
📌 1. DESCRIPCIÓN

Este proyecto es un backend desarrollado en:

Python
Django
Django REST Framework
SQL Server

Permite gestionar:

Usuarios (con roles: atleta, árbitro, etc)
Equipos
Juegos
Plataformas
Trofeos
Hardware (consolas y controles)
Sesiones de entrenamiento
🛠️ 2. REQUISITOS

Instalar:

Python 3.11+
SQL Server (Express o completo)
ODBC Driver 17 o 18
Git (opcional)

📦 3. INSTALACIÓN

🔹 Clonar proyecto
git clone <repo>
cd usuarios_project

🔹 Crear entorno virtual
python -m venv .venv

🔹 Activar entorno
.\.venv\Scripts\activate

🔹 Instalar dependencias
pip install Django djangorestframework python-dotenv mssql-django pyodbc

⚙️ 4. CONFIGURACIÓN

Crear archivo .env en la raíz:

DB_NAME=usuarios_BD
DB_HOST=localhost\SQLEXPRESS
DB_PORT=1433
DB_DRIVER=ODBC Driver 17 for SQL Server

👉 Si usan usuario/contraseña:

DB_USER=usuario
DB_PASSWORD=contraseña
🗄️ 5. BASE DE DATOS
🔥 OPCIÓN RECOMENDADA (PRO)

👉 NO envíes la base de datos

✔ Cada desarrollador debe crearla

🔹 Crear BD en SQL Server
CREATE DATABASE usuarios_BD;

🔹 Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

💥 Esto crea todas las tablas automáticamente

📊 6. DATOS INICIALES (OPCIONAL)

Si necesitas datos de prueba:

python manage.py createsuperuser

▶️ 7. EJECUTAR SERVIDOR
python manage.py runserver

🌐 8. ENDPOINTS

Base URL:

http://127.0.0.1:8000/api/

Ejemplos:

GET /usuarios/
POST /usuarios/
GET /equipos/
POST /sesiones/

🧪 9. PRUEBAS

Se recomienda usar:

Postman
Thunder Client (VS Code)

⚠️ 10. PROBLEMAS COMUNES
❌ No encuentra Django
ModuleNotFoundError: django

👉 Activar entorno virtual:

.\.venv\Scripts\activate

❌ Error SQL Server

👉 Revisar:

Instancia (SQLEXPRESS)
Driver ODBC
Puerto 1433

❌ Error migraciones
python manage.py makemigrations
python manage.py migrate

🧠 11. ARQUITECTURA
models.py → Base de datos
serializers.py → Validación
services.py → Lógica
views.py → Endpoints

🚀 12. BUENAS PRÁCTICAS
No modificar directamente la BD
Siempre usar migraciones
Mantener lógica en services
No poner lógica en views

