import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from proyectos.tests.conftest import UsuarioFactory


@pytest.mark.django_db
def test_login_exitoso_retorna_access_y_refresh():
    usuario = UsuarioFactory(correo='login@test.com')
    usuario.set_password('testpass123')
    usuario.save()

    client = APIClient()
    response = client.post('/api/v1/auth/login/', {
        'correo': 'login@test.com',
        'contrasena': 'testpass123',
    }, format='json')

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert 'usuario' in response.data


@pytest.mark.django_db
def test_login_correo_incorrecto_retorna_401():
    client = APIClient()
    response = client.post('/api/v1/auth/login/', {
        'correo': 'noexiste@test.com',
        'contrasena': 'cualquierclave',
    }, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_contrasena_incorrecta_retorna_401():
    usuario = UsuarioFactory(correo='wrong@test.com')
    usuario.set_password('correcta123')
    usuario.save()

    client = APIClient()
    response = client.post('/api/v1/auth/login/', {
        'correo': 'wrong@test.com',
        'contrasena': 'incorrecta123',
    }, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_acceso_endpoint_sin_token_retorna_401():
    client = APIClient()
    response = client.get('/api/v1/clientes/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_me_retorna_usuario_autenticado(api_client, coordinador):
    response = api_client.get('/api/v1/auth/me/')
    assert response.status_code == 200
    assert response.data['correo'] == coordinador.correo


@pytest.mark.django_db
def test_refresh_token_genera_nuevo_access():
    usuario = UsuarioFactory(correo='refresh@test.com')
    usuario.set_password('testpass123')
    usuario.save()

    refresh = RefreshToken.for_user(usuario)
    client = APIClient()
    response = client.post('/api/v1/auth/token/refresh/', {
        'refresh': str(refresh),
    }, format='json')

    assert response.status_code == 200
    assert 'access' in response.data
