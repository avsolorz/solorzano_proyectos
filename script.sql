# Dentro de la consola psql
CREATE USER solorzano_user WITH PASSWORD 'gestor ';
CREATE DATABASE solorzano_proyecto_db OWNER solorzano_user;
GRANT ALL PRIVILEGES ON DATABASE solorzano_proyecto_db TO solorzano_user;
\q

mkdir -p store/models store/serializers store/views store/tests

touch proyectos/models/__init__.py
touch proyectos/serializers/__init__.py
touch proyectos/views/__init__.py
touch proyectos/tests/__init__.py
touch proyectos/filters.py
touch proyectos/permissions.py