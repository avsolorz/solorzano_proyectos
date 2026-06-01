import pytest


@pytest.mark.django_db
class TestDisenadoresListar:

    def test_listar_disenadores_autenticado_ok(self, admin_client, disenador):
        response = admin_client.get("/api/v1/disenadores/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_listar_disenadores_sin_token_retorna_401(self, api_client, disenador):
        response = api_client.get("/api/v1/disenadores/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestDisenadoresCrear:

    def test_crear_disenador_admin_ok(self, admin_client):
        response = admin_client.post("/api/v1/disenadores/", {
            "nombre": "Carlos Pérez",
            "especialidad": "Ilustración Digital",
            "telefono": "0987654321",
            "correo": "carlos@estudio.com",
        }, format="json")
        assert response.status_code == 201
        assert response.data["nombre"] == "Carlos Pérez"

    def test_crear_disenador_sin_admin_retorna_403(self, gestor_client):
        response = gestor_client.post("/api/v1/disenadores/", {
            "nombre": "Ana Torres",
            "correo": "ana@estudio.com",
        }, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestDisenadoresFiltros:

    def test_filtro_por_especialidad(self, admin_client, disenador):
        response = admin_client.get(
            "/api/v1/disenadores/?especialidad=Diseño Gráfico"
        )
        assert response.status_code == 200
        assert response.data["total"] >= 1
        assert response.data["resultados"][0]["especialidad"] == "Diseño Gráfico"

    def test_filtro_por_especialidad_sin_resultados(self, admin_client, disenador):
        response = admin_client.get(
            "/api/v1/disenadores/?especialidad=Especialidad Inexistente"
        )
        assert response.status_code == 200
        assert response.data["total"] == 0


@pytest.mark.django_db
class TestDisenadoresUnicidad:

    def test_correo_disenador_unico(self, admin_client, disenador):
        response = admin_client.post("/api/v1/disenadores/", {
            "nombre": "Otro Diseñador",
            "correo": "maria@disenio.com",
        }, format="json")
        assert response.status_code == 400
