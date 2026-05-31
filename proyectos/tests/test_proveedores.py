import pytest


@pytest.mark.django_db
class TestProveedorListar:

    def test_admin_puede_listar(self, admin_client, proveedor):
        response = admin_client.get("/api/v1/proveedores/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_colaborador_puede_listar(self, colaborador_client, proveedor):
        response = colaborador_client.get("/api/v1/proveedores/")
        assert response.status_code == 200

    def test_sin_token_no_puede_listar(self, api_client, proveedor):
        response = api_client.get("/api/v1/proveedores/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestProveedorCrear:

    def test_gestor_puede_crear(self, gestor_client):
        response = gestor_client.post("/api/v1/proveedores/", {
            "nombre_empresa": "Sonido Pro S.A.",
            "contacto": "Pedro Ruiz",
            "telefono": "0997654321",
            "correo": "pedroruiz@sonidopro.com",
            "servicio": "Equipos de audio y video",
        }, format="json")
        assert response.status_code == 201
        assert response.data["nombre_empresa"] == "Sonido Pro S.A."

    def test_colaborador_no_puede_crear(self, colaborador_client):
        response = colaborador_client.post("/api/v1/proveedores/", {
            "nombre_empresa": "Proveedor Colab",
            "servicio": "Varios",
        }, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestProveedorEliminar:

    def test_admin_puede_eliminar(self, admin_client, proveedor):
        response = admin_client.delete(f"/api/v1/proveedores/{proveedor.id}/")
        assert response.status_code == 204

    def test_gestor_no_puede_eliminar(self, gestor_client, proveedor):
        response = gestor_client.delete(f"/api/v1/proveedores/{proveedor.id}/")
        assert response.status_code == 403
