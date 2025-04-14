import pytest
from litestar.testing import AsyncTestClient
from app.asgi import app


@pytest.mark.asyncio
async def test_create_user() -> None:
    """Тестирует создание пользователя."""
    async with AsyncTestClient(app=app) as client:
        response = await client.post(
            "/users",
            json={
                "name": "Алексей",
                "surname": "Иванов",
                "password": "secure123",
            },
        )
        if response.status_code != 201:
            print("Error response:", response.text)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Алексей"
        assert data["surname"] == "Иванов"
        assert "password" not in data


@pytest.mark.asyncio
async def test_invalid_user_create() -> None:
    """Тестирует ошибку валидации при создании."""
    async with AsyncTestClient(app=app) as client:
        response = await client.post(
            "/users",
            json={
                "name": " ",
                "surname": "Иванов",
                "password": "123",
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert any(
            error["message"] ==
            "String should match pattern '^\\S.*\\S$|^\\S$'"
            for error in data["extra"]
        )
        assert any(
            error["message"] == "String should have at least 8 characters"
            for error in data["extra"]
        )
