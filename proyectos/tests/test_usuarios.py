import pytest
from rest_framework.test import APIClient
from proyectos.tests.conftest import UsuarioFactory, get_jwt_client


@pytest.mark.django_db
def test_listar_usuarios_admin_ok(admin_client):
    UsuarioFactory.create_batch(3)
    response = admin_client.get('/api/v1/usuarios/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_listar_usuarios_coordinador_retorna_403(api_client):
    response = api_client.get('/api/v1/usuarios/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_crear_usuario_admin_ok(admin_client):
    data = {
        'correo': 'nuevo@test.com',
        'nombre': 'Nuevo',
        'apellido': 'Usuario',
        'rol': 'asistente',
        'contrasena': 'segura1234',
    }
    response = admin_client.post('/api/v1/usuarios/', data, format='json')
    assert response.status_code == 201
    assert response.data['correo'] == 'nuevo@test.com'


@pytest.mark.django_db
def test_cambiar_rol_usuario_ok(admin_client, db):
    usuario = UsuarioFactory(rol='asistente')
    response = admin_client.post(
        f'/api/v1/usuarios/{usuario.id}/cambiar-rol/',
        {'rol': 'coordinador'},
        format='json',
    )
    assert response.status_code == 200
    usuario.refresh_from_db()
    assert usuario.rol == 'coordinador'


@pytest.mark.django_db
def test_cambiar_rol_invalido_retorna_400(admin_client, db):
    usuario = UsuarioFactory(rol='asistente')
    response = admin_client.post(
        f'/api/v1/usuarios/{usuario.id}/cambiar-rol/',
        {'rol': 'superheroe'},
        format='json',
    )
    assert response.status_code == 400
