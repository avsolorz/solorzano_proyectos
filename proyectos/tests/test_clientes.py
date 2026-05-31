import pytest


@pytest.mark.django_db
class TestClienteListar:

    def test_admin_puede_listar(self, admin_client, cliente):
        response = admin_client.get("/api/v1/clientes/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_gestor_puede_listar(self, gestor_client, cliente):
        response = gestor_client.get("/api/v1/clientes/")
        assert response.status_code == 200

    def test_colaborador_puede_listar(self, colaborador_client, cliente):
        response = colaborador_client.get("/api/v1/clientes/")
        assert response.status_code == 200

    def test_sin_token_no_puede_listar(self, api_client, cliente):
        response = api_client.get("/api/v1/clientes/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestClienteCrear:

    def test_admin_puede_crear(self, admin_client):
        response = admin_client.post("/api/v1/clientes/", {
            "nombre": "Empresa XYZ",
            "telefono": "0991111111",
            "correo": "xyz@empresa.com",
            "direccion": "Calle Falsa 123",
        }, format="json")
        assert response.status_code == 201
        assert response.data["nombre"] == "Empresa XYZ"

    def test_gestor_puede_crear(self, gestor_client):
        response = gestor_client.post("/api/v1/clientes/", {
            "nombre": "Empresa Gestor",
            "correo": "gestor@empresa.com",
        }, format="json")
        assert response.status_code == 201

    def test_colaborador_no_puede_crear(self, colaborador_client):
        response = colaborador_client.post("/api/v1/clientes/", {
            "nombre": "Empresa Colab",
        }, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestClienteEliminar:

    def test_admin_puede_eliminar(self, admin_client, cliente):
        response = admin_client.delete(f"/api/v1/clientes/{cliente.id}/")
        assert response.status_code == 204

    def test_gestor_no_puede_eliminar(self, gestor_client, cliente):
        response = gestor_client.delete(f"/api/v1/clientes/{cliente.id}/")
        assert response.status_code == 403
