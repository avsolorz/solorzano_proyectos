import pytest
import factory
from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from proyectos.models import Usuario, Cliente, Evento, Tarea, Proveedor

fake = Faker('es_ES')


class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    nombre = factory.LazyFunction(fake.first_name)
    apellido = factory.LazyFunction(fake.last_name)
    correo = factory.LazyFunction(fake.unique.email)
    rol = 'coordinador'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs.setdefault('password', 'testpass123')
        usuario = model_class(**kwargs)
        usuario.set_password(kwargs.pop('password', 'testpass123'))
        usuario.save()
        return usuario


class ClienteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cliente

    nombre = factory.LazyFunction(fake.company)
    telefono = factory.LazyFunction(fake.phone_number)
    correo = factory.LazyFunction(fake.unique.company_email)
    direccion = factory.LazyFunction(fake.address)


class EventoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Evento

    nombre_evento = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    descripcion = factory.LazyFunction(fake.text)
    fecha_evento = factory.LazyFunction(lambda: fake.future_date(end_date='+1y'))
    ubicacion = factory.LazyFunction(fake.address)
    presupuesto = factory.LazyFunction(lambda: fake.pydecimal(left_digits=6, right_digits=2, positive=True))
    estado = 'planificacion'
    cliente = factory.SubFactory(ClienteFactory)
    coordinador = factory.SubFactory(UsuarioFactory)


class TareaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tarea

    nombre_tarea = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    descripcion = factory.LazyFunction(fake.text)
    fecha_limite = factory.LazyAttribute(lambda obj: obj.evento.fecha_evento)
    prioridad = 'media'
    estado = 'pendiente'
    evento = factory.SubFactory(EventoFactory)


class ProveedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Proveedor

    nombre_empresa = factory.LazyFunction(fake.company)
    contacto = factory.LazyFunction(fake.name)
    telefono = factory.LazyFunction(fake.phone_number)
    correo = factory.LazyFunction(fake.unique.company_email)
    servicio = factory.LazyFunction(lambda: fake.job())


def get_jwt_client(usuario):
    client = APIClient()
    refresh = RefreshToken.for_user(usuario)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client


@pytest.fixture
def usuario_factory(db):
    return UsuarioFactory


@pytest.fixture
def admin_factory(db):
    return lambda **kwargs: UsuarioFactory(rol='admin', **kwargs)


@pytest.fixture
def cliente_factory(db):
    return ClienteFactory


@pytest.fixture
def evento_factory(db):
    return EventoFactory


@pytest.fixture
def tarea_factory(db):
    return TareaFactory


@pytest.fixture
def proveedor_factory(db):
    return ProveedorFactory


@pytest.fixture
def coordinador(db):
    return UsuarioFactory(rol='coordinador')


@pytest.fixture
def admin(db):
    return UsuarioFactory(rol='admin')


@pytest.fixture
def api_client(coordinador):
    return get_jwt_client(coordinador)


@pytest.fixture
def admin_client(admin):
    return get_jwt_client(admin)
