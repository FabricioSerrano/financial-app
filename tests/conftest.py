import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from financial_app.common.database import get_session, tables_registry
from financial_app.common.security import get_password_hash
from financial_app.main import app
from financial_app.users.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    name = factory.LazyAttribute(lambda obj: f'{obj.username}+name')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}+senha')
    role = 'admin'


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    tables_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    tables_registry.metadata.drop_all(engine)

    engine.dispose()


@pytest.fixture
def client(session: Session):
    def get_test_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_test_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session: Session):
    pwd = 'testtest'

    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd

    return user


@pytest.fixture
def other_user(session: Session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
