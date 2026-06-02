import uuid
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from proyectos.models import Usuario, Cliente, Evento, Tarea, Proveedor, RedSocial, Disenador
from datetime import date, timedelta


@pytest.fixture
def api_client():
    return APIClient()


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def get_jwt_client(user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(user)}")
    return client


class UsuarioFactory:
    @staticmethod
    def create(rol="colaborador", username=None, password="Test123!", **kwargs):
        if username is None:
            username = f"user_{uuid.uuid4().hex[:8]}"
        return Usuario.objects.create_user(
            username=username,
            email=f"{username}@test.com",
            password=password,
            rol=rol,
            **kwargs
        )


@pytest.fixture
def admin_user(db):
    return Usuario.objects.create_superuser(
        username="admin_test",
        email="admin@test.com",
        password="Admin123!",
        rol="admin",
    )


@pytest.fixture
def gestor_user(db):
    return Usuario.objects.create_user(
        username="gestor_test",
        email="gestor@test.com",
        password="Gestor123!",
        rol="gestor",
    )


@pytest.fixture
def colaborador_user(db):
    return Usuario.objects.create_user(
        username="colaborador_test",
        email="colaborador@test.com",
        password="Colab123!",
        rol="colaborador",
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(admin_user)}")
    return api_client


@pytest.fixture
def gestor_client(api_client, gestor_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(gestor_user)}")
    return api_client


@pytest.fixture
def colaborador_client(api_client, colaborador_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(colaborador_user)}")
    return api_client


@pytest.fixture
def cliente(db):
    return Cliente.objects.create(
        nombre="Empresa ABC",
        telefono="0991234567",
        correo="contacto@empresaabc.com",
        direccion="Av. Principal 123, Quito",
    )


@pytest.fixture
def evento(db, cliente, gestor_user):
    return Evento.objects.create(
        nombre_evento="Conferencia Anual 2025",
        descripcion="Conferencia de tecnología",
        fecha_evento=date.today() + timedelta(days=30),
        ubicacion="Centro de Convenciones Quito",
        presupuesto=5000.00,
        estado="planificado",
        cliente=cliente,
        usuario=gestor_user,
    )


@pytest.fixture
def tarea(db, evento):
    return Tarea.objects.create(
        nombre_tarea="Reservar salón principal",
        descripcion="Contactar al proveedor del salón",
        fecha_limite=date.today() + timedelta(days=10),
        prioridad="alta",
        estado="pendiente",
        evento=evento,
    )


@pytest.fixture
def proveedor(db):
    return Proveedor.objects.create(
        nombre_empresa="Catering Gourmet S.A.",
        contacto="María López",
        telefono="0998765432",
        correo="info@cateringgourmet.com",
        servicio="Catering y alimentación",
    )


@pytest.fixture
def red_social(db):
    return RedSocial.objects.create(
        nombre_red="Instagram",
    )


@pytest.fixture
def disenador(db):
    return Disenador.objects.create(
        nombre="María García",
        especialidad="Diseño Gráfico",
        telefono="0991234567",
        correo="maria@disenio.com",
    )