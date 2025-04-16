import uuid
from datetime import datetime, UTC
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class User(Base):
    """Модель пользователя."""
    __tablename__ = "user"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name = mapped_column(
        String(length=100),
        nullable=False
    )
    surname = mapped_column(
        String(length=100),
        nullable=False
    )
    password = mapped_column(
        String(length=255),
        nullable=False
    )
    created_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC)
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    def to_dict(self) -> dict:
        """Преобразует объект User в словарь для сериализации."""
        return {
            "id": str(self.id),
            "name": self.name,
            "surname": self.surname,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
