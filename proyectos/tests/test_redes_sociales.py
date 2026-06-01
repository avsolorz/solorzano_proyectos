import pytest


@pytest.mark.django_db
class TestRedSocialListar:

    def test_listar_redes_autenticado_ok(self, admin_client, red_social):
        response = admin_client.get("/api/v1/redes-sociales/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_listar_redes_sin_token_retorna_401(self, api_client, red_social):
        response = api_client.get("/api/v1/redes-sociales/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestRedSocialCrear:

    def test_crear_red_admin_ok(self, admin_client):
        response = admin_client.post("/api/v1/redes-sociales/", {
            "nombre_red": "Facebook",
        }, format="json")
        assert response.status_code == 201
        assert response.data["nombre_red"] == "Facebook"

    def test_crear_red_coordinador_retorna_403(self, gestor_client):
        response = gestor_client.post("/api/v1/redes-sociales/", {
            "nombre_red": "TikTok",
        }, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestRedSocialUnicidad:

    def test_nombre_red_unico(self, admin_client, red_social):
        response = admin_client.post("/api/v1/redes-sociales/", {
            "nombre_red": "Instagram",
        }, format="json")
        assert response.status_code == 400
