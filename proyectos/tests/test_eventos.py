import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from proyectos.tests.conftest import (
    UsuarioFactory,
    ClienteFactory,
    EventoFactory,
    TareaFactory,
    get_jwt_client,
)


@pytest.mark.django_db
def test_admin_ve_todos_los_eventos(admin_client, db):
    coord1 = UsuarioFactory(rol='coordinador')
    coord2 = UsuarioFactory(rol='coordinador')
    EventoFactory(coordinador=coord1)
    EventoFactory(coordinador=coord2)
    response = admin_client.get('/api/v1/eventos/')
    assert response.status_code == 200
    assert response.data['count'] >= 2


@pytest.mark.django_db
def test_coordinador_solo_ve_sus_eventos(coordinador, db):
    otro_coord = UsuarioFactory(rol='coordinador')
    EventoFactory(coordinador=coordinador)
    EventoFactory(coordinador=otro_coord)

    client = get_jwt_client(coordinador)
    response = client.get('/api/v1/eventos/')
    assert response.status_code == 200
    assert response.data['count'] == 1


@pytest.mark.django_db
def test_crear_evento_coordinador_ok(api_client, coordinador, db):
    cliente = ClienteFactory()
    data = {
        'nombre_evento': 'Evento Test',
        'fecha_evento': str(date.today() + timedelta(days=30)),
        'cliente': cliente.id,
        'coordinador': coordinador.id,
        'estado': 'planificacion',
    }
    response = api_client.post('/api/v1/eventos/', data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_crear_evento_fecha_pasada_retorna_400(api_client, coordinador, db):
    cliente = ClienteFactory()
    data = {
        'nombre_evento': 'Evento Pasado',
        'fecha_evento': str(date.today() - timedelta(days=1)),
        'cliente': cliente.id,
        'coordinador': coordinador.id,
    }
    response = api_client.post('/api/v1/eventos/', data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_actualizar_evento_propietario_ok(coordinador, db):
    evento = EventoFactory(coordinador=coordinador)
    client = get_jwt_client(coordinador)
    response = client.patch(
        f'/api/v1/eventos/{evento.id}/',
        {'estado': 'en_proceso'},
        format='json',
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_actualizar_evento_otro_coordinador_retorna_403(db):
    coord1 = UsuarioFactory(rol='coordinador')
    coord2 = UsuarioFactory(rol='coordinador')
    evento = EventoFactory(coordinador=coord1)

    client = get_jwt_client(coord2)
    response = client.patch(
        f'/api/v1/eventos/{evento.id}/',
        {'estado': 'en_proceso'},
        format='json',
    )
    # El queryset filtra por coordinador propietario, coord2 recibe 404 (evento no visible)
    assert response.status_code == 404


@pytest.mark.django_db
def test_listar_tareas_de_evento(api_client, coordinador, db):
    evento = EventoFactory(coordinador=coordinador)
    TareaFactory.create_batch(3, evento=evento)
    response = api_client.get(f'/api/v1/eventos/{evento.id}/tareas/')
    assert response.status_code == 200
    assert response.data['count'] == 3


@pytest.mark.django_db
def test_filtro_por_estado(admin_client, db):
    EventoFactory(estado='planificacion')
    EventoFactory(estado='completado')
    response = admin_client.get('/api/v1/eventos/?estado=planificacion')
    assert response.status_code == 200
    for evento in response.data['results']:
        assert evento['estado'] == 'planificacion'


@pytest.mark.django_db
def test_filtro_por_rango_fechas(admin_client, db):
    hoy = date.today()
    EventoFactory(fecha_evento=hoy + timedelta(days=10))
    EventoFactory(fecha_evento=hoy + timedelta(days=60))

    desde = str(hoy + timedelta(days=5))
    hasta = str(hoy + timedelta(days=30))
    response = admin_client.get(f'/api/v1/eventos/?fecha_evento_desde={desde}&fecha_evento_hasta={hasta}')
    assert response.status_code == 200
    assert response.data['count'] == 1
