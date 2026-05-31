-- Script SQL para la base de datos del Gestor de Proyectos de Eventos
-- Compatible con PostgreSQL

CREATE TABLE usuarios (
    id_usuario  SERIAL PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    correo      VARCHAR(255) UNIQUE NOT NULL,
    contrasena  VARCHAR(255) NOT NULL,
    rol         VARCHAR(20) CHECK (rol IN ('admin', 'coordinador', 'asistente'))
                DEFAULT 'asistente'
);

CREATE TABLE clientes (
    id_cliente  SERIAL PRIMARY KEY,
    nombre      VARCHAR(150) NOT NULL,
    telefono    VARCHAR(20),
    correo      VARCHAR(255) UNIQUE NOT NULL,
    direccion   TEXT
);

CREATE TABLE eventos (
    id_evento      SERIAL PRIMARY KEY,
    nombre_evento  VARCHAR(200) NOT NULL,
    descripcion    TEXT,
    fecha_evento   DATE NOT NULL,
    ubicacion      VARCHAR(255),
    presupuesto    DECIMAL(12, 2),
    estado         VARCHAR(20) CHECK (estado IN
                   ('planificacion', 'en_proceso', 'completado', 'cancelado'))
                   DEFAULT 'planificacion',
    id_cliente     INT REFERENCES clientes(id_cliente) ON DELETE RESTRICT,
    id_usuario     INT REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

CREATE TABLE tareas (
    id_tarea      SERIAL PRIMARY KEY,
    nombre_tarea  VARCHAR(200) NOT NULL,
    descripcion   TEXT,
    fecha_limite  DATE NOT NULL,
    prioridad     VARCHAR(10) CHECK (prioridad IN ('alta', 'media', 'baja'))
                  DEFAULT 'media',
    estado        VARCHAR(20) CHECK (estado IN
                  ('pendiente', 'en_progreso', 'completada'))
                  DEFAULT 'pendiente',
    id_evento     INT REFERENCES eventos(id_evento) ON DELETE CASCADE
);

CREATE TABLE proveedores (
    id_proveedor   SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(200) NOT NULL,
    contacto       VARCHAR(150),
    telefono       VARCHAR(20),
    correo         VARCHAR(255) UNIQUE NOT NULL,
    servicio       VARCHAR(200)
);
