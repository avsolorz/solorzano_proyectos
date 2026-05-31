import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from proyectos.models import Usuario, Cliente, Evento, Tarea, Proveedor
from datetime import date, timedelta


# ------------------------------------------------------------------
# Clientes autenticados
# ------------------------------------------------------------------
@pytest.fixture
def api_client():
    return APIClient()


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


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


# ------------------------------------------------------------------
# Fixtures de modelos
# ------------------------------------------------------------------
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
