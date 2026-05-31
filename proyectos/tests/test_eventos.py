import pytest
from datetime import date, timedelta
from proyectos.models import Evento


@pytest.mark.django_db
class TestEventoListar:

    def test_admin_puede_listar(self, admin_client, evento):
        response = admin_client.get("/api/v1/eventos/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_colaborador_puede_listar(self, colaborador_client, evento):
        response = colaborador_client.get("/api/v1/eventos/")
        assert response.status_code == 200

    def test_sin_token_no_puede_listar(self, api_client, evento):
        response = api_client.get("/api/v1/eventos/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestEventoCrear:

    def test_gestor_puede_crear(self, gestor_client, cliente, gestor_user):
        response = gestor_client.post("/api/v1/eventos/", {
            "nombre_evento": "Workshop Tecnología",
            "descripcion": "Taller intensivo",
            "fecha_evento": str(date.today() + timedelta(days=20)),
            "ubicacion": "Sala A",
            "presupuesto": "2000.00",
            "estado": "planificado",
            "cliente": cliente.id,
            "usuario": gestor_user.id,
        }, format="json")
        assert response.status_code == 201
        assert response.data["nombre_evento"] == "Workshop Tecnología"

    def test_colaborador_no_puede_crear(self, colaborador_client, cliente, gestor_user):
        response = colaborador_client.post("/api/v1/eventos/", {
            "nombre_evento": "Evento Colab",
            "fecha_evento": str(date.today() + timedelta(days=5)),
            "cliente": cliente.id,
            "usuario": gestor_user.id,
        }, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestEventoCambiarEstado:

    def test_gestor_puede_cambiar_estado(self, gestor_client, evento):
        url = f"/api/v1/eventos/{evento.id}/cambiar-estado/"
        response = gestor_client.patch(url, {"estado": "en_progreso"}, format="json")
        assert response.status_code == 200
        assert response.data["estado"] == "en_progreso"

    def test_estado_invalido_falla(self, gestor_client, evento):
        url = f"/api/v1/eventos/{evento.id}/cambiar-estado/"
        response = gestor_client.patch(url, {"estado": "inexistente"}, format="json")
        assert response.status_code == 400

    def test_colaborador_no_puede_cambiar_estado(self, colaborador_client, evento):
        url = f"/api/v1/eventos/{evento.id}/cambiar-estado/"
        response = colaborador_client.patch(url, {"estado": "completado"}, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestEventoPorCliente:

    def test_buscar_por_cliente(self, gestor_client, evento, cliente):
        response = gestor_client.get(f"/api/v1/eventos/por-cliente/?cliente_id={cliente.id}")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_sin_parametro_falla(self, gestor_client):
        response = gestor_client.get("/api/v1/eventos/por-cliente/")
        assert response.status_code == 400
