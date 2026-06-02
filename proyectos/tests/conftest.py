import uuid
import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from proyectos.models import Usuario, Cliente, Evento, Tarea, Proveedor, RedSocial, Disenador


# ─── Helpers ────────────────────────────────────────────────────────────────

def get_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def get_jwt_client(user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(user)}")
    return client


# ─── Factories ──────────────────────────────────────────────────────────────

class UsuarioFactory:
    @staticmethod
    def create(rol="asistente", username=None, password="Test123!", **kwargs):
        if username is None:
            username = f"user_{uuid.uuid4().hex[:8]}"
        return Usuario.objects.create_user(
            username=username,
            email=f"{username}@test.com",
            password=password,
            rol=rol,
            **kwargs
        )

    @staticmethod
    def create_batch(n, **kwargs):
        return [UsuarioFactory.create(**kwargs) for _ in range(n)]

    def __call__(self, **kwargs):
        return UsuarioFactory.create(**kwargs)


class ClienteFactory:
    @staticmethod
    def create(**kwargs):
        defaults = dict(
            nombre=f"Empresa_{uuid.uuid4().hex[:6]}",
            telefono="0991234567",
            correo=f"contacto_{uuid.uuid4().hex[:6]}@test.com",
            direccion="Av. Principal 123, Quito",
        )
        defaults.update(kwargs)
        return Cliente.objects.create(**defaults)

    def __call__(self, **kwargs):
        return ClienteFactory.create(**kwargs)


class EventoFactory:
    @staticmethod
    def create(**kwargs):
        if "cliente" not in kwargs:
            kwargs["cliente"] = ClienteFactory.create()
        if "usuario" not in kwargs:
            kwargs["usuario"] = UsuarioFactory.create(rol="coordinador")
        defaults = dict(
            nombre_evento=f"Evento_{uuid.uuid4().hex[:6]}",
            descripcion="Descripción de prueba",
            fecha_evento=date.today() + timedelta(days=30),
            ubicacion="Quito, Ecuador",
            presupuesto=5000.00,
            estado="planificacion",
        )
        defaults.update(kwargs)
        return Evento.objects.create(**defaults)

    def __call__(self, **kwargs):
        return EventoFactory.create(**kwargs)


class TareaFactory:
    @staticmethod
    def create(**kwargs):
        if "evento" not in kwargs:
            kwargs["evento"] = EventoFactory.create()
        defaults = dict(
            nombre_tarea=f"Tarea_{uuid.uuid4().hex[:6]}",
            descripcion="Descripción de tarea",
            fecha_limite=date.today() + timedelta(days=10),
            prioridad="alta",
            estado="pendiente",
        )
        defaults.update(kwargs)
        return Tarea.objects.create(**defaults)

    def __call__(self, **kwargs):
        return TareaFactory.create(**kwargs)


class ProveedorFactory:
    @staticmethod
    def create(**kwargs):
        defaults = dict(
            nombre_empresa=f"Proveedor_{uuid.uuid4().hex[:6]}",
            contacto="Contacto Test",
            telefono="0998765432",
            correo=f"proveedor_{uuid.uuid4().hex[:6]}@test.com",
            servicio="Servicio general",
        )
        defaults.update(kwargs)
        return Proveedor.objects.create(**defaults)

    def __call__(self, **kwargs):
        return ProveedorFactory.create(**kwargs)


# ─── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture
def api_client():
    return APIClient()


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
def admin_client(db, api_client, admin_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(admin_user)}")
    return api_client


@pytest.fixture
def gestor_client(db, api_client, gestor_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(gestor_user)}")
    return api_client


@pytest.fixture
def colaborador_client(db, api_client, colaborador_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(colaborador_user)}")
    return api_client


@pytest.fixture
def cliente(db):
    return ClienteFactory.create(
        nombre="Empresa ABC",
        telefono="0991234567",
        correo="contacto@empresaabc.com",
        direccion="Av. Principal 123, Quito",
    )


@pytest.fixture
def evento(db, cliente, gestor_user):
    return EventoFactory.create(
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
    return TareaFactory.create(
        nombre_tarea="Reservar salón principal",
        descripcion="Contactar al proveedor del salón",
        fecha_limite=date.today() + timedelta(days=10),
        prioridad="alta",
        estado="pendiente",
        evento=evento,
    )


@pytest.fixture
def proveedor(db):
    return ProveedorFactory.create(
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