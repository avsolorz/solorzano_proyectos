import pytest
from rest_framework.test import APIClient
from proyectos.tests.conftest import ClienteFactory


@pytest.mark.django_db
def test_listar_clientes_coordinador_ok(api_client):
    ClienteFactory.create_batch(3)
    response = api_client.get('/api/v1/clientes/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_listar_clientes_sin_auth_retorna_401():
    client = APIClient()
    response = client.get('/api/v1/clientes/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_crear_cliente_admin_ok(admin_client):
    data = {
        'nombre': 'Cliente Nuevo',
        'correo': 'cliente@nuevo.com',
        'telefono': '0991234567',
        'direccion': 'Av. Principal 123',
    }
    response = admin_client.post('/api/v1/clientes/', data, format='json')
    assert response.status_code == 201
    assert response.data['nombre'] == 'Cliente Nuevo'


@pytest.mark.django_db
def test_crear_cliente_coordinador_retorna_403(api_client):
    data = {
        'nombre': 'Cliente No Permitido',
        'correo': 'nopermitido@test.com',
    }
    response = api_client.post('/api/v1/clientes/', data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db
def test_actualizar_cliente_admin_ok(admin_client):
    cliente = ClienteFactory()
    response = admin_client.patch(
        f'/api/v1/clientes/{cliente.id}/',
        {'nombre': 'Nombre Actualizado'},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['nombre'] == 'Nombre Actualizado'


@pytest.mark.django_db
def test_eliminar_cliente_admin_ok(admin_client):
    cliente = ClienteFactory()
    response = admin_client.delete(f'/api/v1/clientes/{cliente.id}/')
    assert response.status_code == 204


@pytest.mark.django_db
def test_filtro_por_nombre(api_client):
    ClienteFactory(nombre='Empresa Alpha')
    ClienteFactory(nombre='Empresa Beta')
    response = api_client.get('/api/v1/clientes/?nombre=Alpha')
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['nombre'] == 'Empresa Alpha'


@pytest.mark.django_db
def test_paginacion_page_size(api_client):
    ClienteFactory.create_batch(15)
    response = api_client.get('/api/v1/clientes/?page_size=5')
    assert response.status_code == 200
    assert len(response.data['results']) == 5
