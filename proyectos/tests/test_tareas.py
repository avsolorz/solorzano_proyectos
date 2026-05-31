import pytest
from datetime import timedelta
from proyectos.tests.conftest import EventoFactory, TareaFactory


@pytest.mark.django_db
def test_crear_tarea_valida_ok(api_client, coordinador, db):
    evento = EventoFactory(coordinador=coordinador)
    data = {
        'nombre_tarea': 'Preparar decoración',
        'fecha_limite': str(evento.fecha_evento),
        'prioridad': 'alta',
        'estado': 'pendiente',
        'evento': evento.id,
    }
    response = api_client.post('/api/v1/tareas/', data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_fecha_limite_anterior_a_evento_retorna_400(api_client, coordinador, db):
    evento = EventoFactory(coordinador=coordinador)
    data = {
        'nombre_tarea': 'Tarea Inválida',
        'fecha_limite': str(evento.fecha_evento - timedelta(days=5)),
        'prioridad': 'media',
        'estado': 'pendiente',
        'evento': evento.id,
    }
    response = api_client.post('/api/v1/tareas/', data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_cambiar_estado_tarea_ok(api_client, coordinador, db):
    evento = EventoFactory(coordinador=coordinador)
    tarea = TareaFactory(evento=evento, estado='pendiente')
    response = api_client.patch(
        f'/api/v1/tareas/{tarea.id}/cambiar-estado/',
        {'estado': 'en_progreso'},
        format='json',
    )
    assert response.status_code == 200
    tarea.refresh_from_db()
    assert tarea.estado == 'en_progreso'


@pytest.mark.django_db
def test_filtro_por_prioridad(api_client, coordinador, db):
    evento = EventoFactory(coordinador=coordinador)
    TareaFactory(evento=evento, prioridad='alta')
    TareaFactory(evento=evento, prioridad='baja')
    response = api_client.get('/api/v1/tareas/?prioridad=alta')
    assert response.status_code == 200
    for tarea in response.data['results']:
        assert tarea['prioridad'] == 'alta'


@pytest.mark.django_db
def test_filtro_por_evento_id(api_client, coordinador, db):
    evento1 = EventoFactory(coordinador=coordinador)
    evento2 = EventoFactory(coordinador=coordinador)
    TareaFactory.create_batch(2, evento=evento1)
    TareaFactory(evento=evento2)
    response = api_client.get(f'/api/v1/tareas/?evento_id={evento1.id}')
    assert response.status_code == 200
    assert response.data['count'] == 2
