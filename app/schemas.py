from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_serializer


NON_EMPTY_PATTERN = r"^\S.*\S$|^\S$"
MAX_NAME_LENGTH = 50
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 100


class UserCreate(BaseModel):
    """Схема для создания пользователя."""
    name: str = Field(
        max_length=MAX_NAME_LENGTH,
        pattern=NON_EMPTY_PATTERN
    )
    surname: str = Field(
        max_length=MAX_NAME_LENGTH,
        pattern=NON_EMPTY_PATTERN
    )
    password: str = Field(
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
    )


class UserUpdate(BaseModel):
    """Схема для обновления пользователя."""
    name: str | None = Field(
        default=None,
        max_length=MAX_NAME_LENGTH,
        pattern=NON_EMPTY_PATTERN,
    )
    surname: str | None = Field(
        default=None,
        max_length=MAX_NAME_LENGTH,
        pattern=NON_EMPTY_PATTERN,
    )
    password: str | None = Field(
        default=None,
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
    )


class UserRead(BaseModel):
    """Схема для чтения пользователя."""
    id: str
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime

    @field_serializer
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat()

    model_config = ConfigDict()
