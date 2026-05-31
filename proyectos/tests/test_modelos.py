import pytest
from proyectos.tests.conftest import (
    UsuarioFactory,
    ClienteFactory,
    EventoFactory,
    TareaFactory,
    ProveedorFactory,
)
from proyectos.models import Usuario, Evento, Tarea


@pytest.mark.django_db
def test_str_usuario():
    usuario = UsuarioFactory(nombre='Ana', apellido='García', rol='admin')
    assert str(usuario) == 'Ana García (admin)'


@pytest.mark.django_db
def test_str_cliente():
    cliente = ClienteFactory(nombre='Empresa XYZ')
    assert str(cliente) == 'Empresa XYZ'


@pytest.mark.django_db
def test_str_evento():
    evento = EventoFactory(nombre_evento='Boda Real', estado='planificacion')
    assert 'Boda Real' in str(evento)
    assert 'Planificación' in str(evento)


@pytest.mark.django_db
def test_str_tarea():
    tarea = TareaFactory(nombre_tarea='Reservar salón', prioridad='alta')
    assert 'Reservar salón' in str(tarea)
    assert 'Alta' in str(tarea)


@pytest.mark.django_db
def test_str_proveedor():
    proveedor = ProveedorFactory(nombre_empresa='Catering Elite', servicio='Catering')
    assert 'Catering Elite' in str(proveedor)
    assert 'Catering' in str(proveedor)


@pytest.mark.django_db
def test_evento_relacionado_con_cliente():
    cliente = ClienteFactory()
    evento = EventoFactory(cliente=cliente)
    assert evento.cliente == cliente
    assert evento in cliente.eventos.all()


@pytest.mark.django_db
def test_tarea_relacionada_con_evento():
    evento = EventoFactory()
    tarea = TareaFactory(evento=evento)
    assert tarea.evento == evento
    assert tarea in evento.tareas.all()


@pytest.mark.django_db
def test_choices_rol_usuario():
    roles = [r[0] for r in Usuario.ROL_CHOICES]
    assert 'admin' in roles
    assert 'coordinador' in roles
    assert 'asistente' in roles


@pytest.mark.django_db
def test_choices_estado_evento():
    estados = [e[0] for e in Evento.ESTADO_CHOICES]
    assert 'planificacion' in estados
    assert 'en_proceso' in estados
    assert 'completado' in estados
    assert 'cancelado' in estados


@pytest.mark.django_db
def test_choices_prioridad_tarea():
    prioridades = [p[0] for p in Tarea.PRIORIDAD_CHOICES]
    assert 'alta' in prioridades
    assert 'media' in prioridades
    assert 'baja' in prioridades
