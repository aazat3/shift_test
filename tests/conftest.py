from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import event


from shift_test.src.db.base import Base
from shift_test.src.db.session import get_session
from shift_test.src.main import app



DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(DATABASE_URL, echo=True)

@event.listens_for(async_engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

async_session_test = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="module", autouse=True)
async def prepare_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session():
    async with async_session_test() as session:
        yield session
    
    async with async_engine.begin() as conn:
        for table in reversed(
            Base.metadata.sorted_tables
        ):
            await conn.execute(
                table.delete()
            )

    
@pytest_asyncio.fixture
async def async_client(session):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(
    async_client: AsyncClient
):
    await async_client.post(
        "/api/auth/register",
        json={
            "username": "user",
            "password": "123"
        }
    )

    response = await async_client.post(
        "/api/auth/login",
        json={
            "username": "user",
            "password": "123"
        }
    )

    assert response.status_code == 200

    assert (
        "users_access_token"
        in async_client.cookies
    )

    return async_client