from pydantic import ValidationError
from app.schemas import UserCreate


def test_valid_user_create() -> None:
    """Тестирует успешное создание пользователя."""
    user = UserCreate(
        name="Алексей",
        surname="Иванов",
        password="secure123",
    )
    assert user.name == "Алексей"
    assert user.surname == "Иванов"
    assert user.password == "secure123"


def test_invalid_user_create() -> None:
    """Тестирует ошибку валидации для невалидных данных."""
    try:
        UserCreate(
            name=" ",
            surname="Иванов",
            password="123",
        )
        assert False, "Ожидалась ошибка валидации"
    except ValidationError as e:
        assert "string_pattern_mismatch" in str(e)
        assert "string_too_short" in str(e)
