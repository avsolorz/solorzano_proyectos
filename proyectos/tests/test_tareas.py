import pytest
from datetime import date, timedelta
from proyectos.models import Tarea


@pytest.mark.django_db
class TestTareaListar:

    def test_admin_puede_listar(self, admin_client, tarea):
        response = admin_client.get("/api/v1/tareas/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_colaborador_puede_listar(self, colaborador_client, tarea):
        response = colaborador_client.get("/api/v1/tareas/")
        assert response.status_code == 200

    def test_sin_token_no_puede_listar(self, api_client, tarea):
        response = api_client.get("/api/v1/tareas/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestTareaCrear:

    def test_gestor_puede_crear(self, gestor_client, evento):
        response = gestor_client.post("/api/v1/tareas/", {
            "nombre_tarea": "Preparar materiales",
            "descripcion": "Imprimir folletos y presentaciones",
            "fecha_limite": str(date.today() + timedelta(days=7)),
            "prioridad": "media",
            "estado": "pendiente",
            "evento": evento.id,
        }, format="json")
        assert response.status_code == 201
        assert response.data["nombre_tarea"] == "Preparar materiales"

    def test_colaborador_no_puede_crear(self, colaborador_client, evento):
        response = colaborador_client.post("/api/v1/tareas/", {
            "nombre_tarea": "Tarea Colab",
            "prioridad": "baja",
            "estado": "pendiente",
            "evento": evento.id,
        }, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestTareaCambiarEstado:

    def test_gestor_puede_cambiar_estado(self, gestor_client, tarea):
        url = f"/api/v1/tareas/{tarea.id}/cambiar-estado/"
        response = gestor_client.patch(url, {"estado": "en_progreso"}, format="json")
        assert response.status_code == 200
        assert response.data["estado"] == "en_progreso"

    def test_estado_invalido_falla(self, gestor_client, tarea):
        url = f"/api/v1/tareas/{tarea.id}/cambiar-estado/"
        response = gestor_client.patch(url, {"estado": "hecho"}, format="json")
        assert response.status_code == 400

    def test_colaborador_no_puede_cambiar_estado(self, colaborador_client, tarea):
        url = f"/api/v1/tareas/{tarea.id}/cambiar-estado/"
        response = colaborador_client.patch(url, {"estado": "completada"}, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestTareaEliminar:

    def test_admin_puede_eliminar(self, admin_client, tarea):
        response = admin_client.delete(f"/api/v1/tareas/{tarea.id}/")
        assert response.status_code == 204

    def test_gestor_no_puede_eliminar(self, gestor_client, tarea):
        response = gestor_client.delete(f"/api/v1/tareas/{tarea.id}/")
        assert response.status_code == 403
