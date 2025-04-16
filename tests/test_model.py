import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


@pytest.mark.asyncio
async def test_user_creation(db_session: AsyncSession) -> None:
    """Тестирует создание объекта User и его сохранение в базе."""
    # Создаём объект User
    user = User(
        name="Алексей",
        surname="Иванов",
        password="secure123",
    )

    db_session.add(user)
    await db_session.commit()

    saved_user = await db_session.get(User, user.id)
    assert saved_user is not None
    assert isinstance(saved_user.id, (str, type(uuid.uuid4())))
    assert saved_user.name == "Алексей"
    assert saved_user.surname == "Иванов"
    assert saved_user.password == "secure123"
    assert isinstance(saved_user.created_at, datetime)
    assert isinstance(saved_user.updated_at, datetime)
    assert saved_user.created_at.tzinfo is not None
    assert saved_user.updated_at.tzinfo is not None
    assert saved_user.created_at == user.created_at
    assert saved_user.updated_at == user.updated_at


@pytest.mark.asyncio
async def test_user_update(db_session: AsyncSession) -> None:
    """Тестирует обновление пользователя и поле updated_at."""
    # Создаём и сохраняем пользователя
    user = User(
        name="Алексей",
        surname="Иванов",
        password="secure123",
    )
    db_session.add(user)
    await db_session.commit()

    # Сохраняем начальное значение updated_at
    original_updated_at = user.updated_at

    # Обновляем пользователя
    user.name = "Михаил"
    await db_session.commit()

    # Извлекаем обновлённого пользователя
    updated_user = await db_session.get(User, user.id)
    assert updated_user is not None
    assert updated_user.name == "Михаил"
    assert updated_user.updated_at > original_updated_at
    assert updated_user.created_at == user.created_at


@pytest.mark.asyncio
async def test_user_required_fields(db_session: AsyncSession) -> None:
    """Тестирует, что обязательные поля не могут быть NULL."""
    user = User(name=None, surname="Иванов", password="secure123")
    db_session.add(user)
    with pytest.raises(Exception) as exc_info:
        await db_session.commit()
    assert "null value in column" in str(exc_info.value)
    await db_session.rollback()
