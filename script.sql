# Dentro de la consola psql
CREATE USER solorzano_user WITH PASSWORD 'gestor ';
CREATE DATABASE solorzano_proyecto_db OWNER solorzano_user;
GRANT ALL PRIVILEGES ON DATABASE solorzano_proyecto_db TO solorzano_user;
\q

mkdir -p store/models store/serializers store/views store/tests

touch cursos/models/__init__.py
touch cursos/serializers/__init__.py
touch cursos/views/__init__.py
touch cursos/tests/__init__.py
touch cursos/filters.py
touch cursos/permissions.py