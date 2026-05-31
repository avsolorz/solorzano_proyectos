import pytest
from proyectos.models import Usuario


@pytest.mark.django_db
class TestLogin:

    def test_login_exitoso(self, api_client, admin_user):
        response = api_client.post("/api/v1/auth/login/", {
            "username": "admin_test",
            "password": "Admin123!",
        }, format="json")
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["usuario"]["rol"] == "admin"

    def test_login_credenciales_invalidas(self, api_client, admin_user):
        response = api_client.post("/api/v1/auth/login/", {
            "username": "admin_test",
            "password": "WrongPass!",
        }, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestRegistro:

    def test_registro_exitoso(self, api_client):
        response = api_client.post("/api/v1/auth/registro/", {
            "username": "nuevo_usuario",
            "email": "nuevo@test.com",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "rol": "colaborador",
            "password": "NuevoPass123!",
            "password2": "NuevoPass123!",
        }, format="json")
        assert response.status_code == 201
        assert "access" in response.data

    def test_registro_passwords_no_coinciden(self, api_client):
        response = api_client.post("/api/v1/auth/registro/", {
            "username": "otro_usuario",
            "email": "otro@test.com",
            "password": "Pass123!",
            "password2": "OtroPass123!",
        }, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestPerfil:

    def test_ver_perfil_autenticado(self, admin_client):
        response = admin_client.get("/api/v1/auth/perfil/")
        assert response.status_code == 200
        assert response.data["username"] == "admin_test"
        assert response.data["rol"] == "admin"

    def test_ver_perfil_sin_token(self, api_client):
        response = api_client.get("/api/v1/auth/perfil/")
        assert response.status_code == 401
