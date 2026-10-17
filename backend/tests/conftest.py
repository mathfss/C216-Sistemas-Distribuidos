import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.models.item import Item

# Banco de dados SQLite em memoria isolado para testes
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Cria tabelas e insere dados iniciais antes de cada teste."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    initial_items = [
        Item(
            id=1,
            name="Servidor Node A",
            description="No do cluster distribuido",
            price=1500.0,
        ),
        Item(
            id=2,
            name="Servidor Node B",
            description="No de processamento",
            price=2200.0,
        ),
        Item(id=3, name="Load Balancer", description="Distribuidor de carga", price=800.0),
    ]
    db.add_all(initial_items)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """Fornece uma sessao isolada para testes unitarios."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Fornece o TestClient com a dependencia get_db apontando para o banco de testes."""

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_item_payload():
    """Payload padrao para criacao de item."""
    return {
        "name": "Cluster Worker",
        "description": "No de computacao distribuida",
        "price": 1250.00,
    }
