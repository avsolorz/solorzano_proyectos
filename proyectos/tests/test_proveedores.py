import pytest
from rest_framework.test import APIClient
from proyectos.tests.conftest import ProveedorFactory


@pytest.mark.django_db
def test_listar_proveedores_autenticado_ok(api_client):
    ProveedorFactory.create_batch(3)
    response = api_client.get('/api/v1/proveedores/')
    assert response.status_code == 200
    assert response.data['count'] >= 3


@pytest.mark.django_db
def test_listar_proveedores_sin_auth_retorna_401():
    client = APIClient()
    response = client.get('/api/v1/proveedores/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_crear_proveedor_admin_ok(admin_client):
    data = {
        'nombre_empresa': 'Catering Premium S.A.',
        'contacto': 'Juan Pérez',
        'telefono': '0997654321',
        'correo': 'catering@premium.com',
        'servicio': 'Catering y banquetes',
    }
    response = admin_client.post('/api/v1/proveedores/', data, format='json')
    assert response.status_code == 201
    assert response.data['nombre_empresa'] == 'Catering Premium S.A.'


@pytest.mark.django_db
def test_crear_proveedor_coordinador_retorna_403(api_client):
    data = {
        'nombre_empresa': 'Proveedor No Permitido',
        'correo': 'nopermitido@proveedor.com',
    }
    response = api_client.post('/api/v1/proveedores/', data, format='json')
    assert response.status_code == 403
