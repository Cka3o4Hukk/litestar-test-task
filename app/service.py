import logging
from uuid import UUID

from litestar.exceptions import HTTPException
from sqlalchemy.sql import select

from app.models import User
from app.repository import UserRepository
from app.schemas import UserCreate, UserRead, UserUpdate

logger = logging.getLogger(__name__)

HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404


def raise_http_exception(status_code: int, detail: str) -> None:
    """Выбрасывает HTTPException с указанным статус-кодом и сообщением."""
    raise HTTPException(status_code=status_code, detail=detail)


async def create_user(data: UserCreate, user_repo: UserRepository) -> UserRead:
    """Создаёт нового пользователя."""
    try:
        async with user_repo.session.begin():
            user = await user_repo.add(User(**data.model_dump()))
            await user_repo.session.refresh(user)
            logger.info(f"User created: {user.id}")
            return UserRead.model_validate(user.to_dict())
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}", exc_info=True)
        raise


async def list_users(
    user_repo: UserRepository,
    limit: int = 100,
    offset: int = 0
) -> list[UserRead]:
    """Возвращает список всех пользователей."""
    try:
        statement = select(User).limit(limit).offset(offset)
        users = await user_repo.list(statement=statement)
        if not users:
            logger.info("No users found in the database")
        return [UserRead.model_validate(user.to_dict()) for user in users]
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}", exc_info=True)
        raise


async def get_user(user_id: str, user_repo: UserRepository) -> UserRead:
    """Возвращает пользователя по ID."""
    try:
        UUID(user_id)  # ValueError, если формат некорректен
        user = await user_repo.get_one_or_none(id=user_id)
        if user is None:
            raise_http_exception(
                HTTP_404_NOT_FOUND,
                f"Пользователь с ID {user_id} не найден"
            )
        return UserRead.model_validate(user.to_dict())
    except HTTPException as e:
        logger.warning(f"User not found: {str(e)}")
        raise
    except ValueError:
        raise_http_exception(
            HTTP_400_BAD_REQUEST,
            f"Некорректный формат ID: {user_id}"
        )
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {str(e)}", exc_info=True)
        raise


async def update_user(
    user_id: str,
    data: UserUpdate,
    user_repo: UserRepository,
) -> UserRead:
    """Обновляет пользователя по ID."""
    try:
        UUID(user_id)
        user = await user_repo.get_one_or_none(id=user_id)
        if user is None:
            raise_http_exception(
                HTTP_404_NOT_FOUND,
                f"Пользователь с ID {user_id} не найден"
            )
        user_dict = data.model_dump(exclude_unset=True)
        if not user_dict:
            raise_http_exception(
                HTTP_400_BAD_REQUEST,
                "Не указаны данные для обновления"
            )
        logger.info(f"Updating user {user_id} with data: {user_dict}")
        for key, value in user_dict.items():
            setattr(user, key, value)
        user = await user_repo.update(user)
        await user_repo.session.commit()
        await user_repo.session.refresh(user)
        logger.info(f"User updated: {user.to_dict()}")
        return UserRead.model_validate(user.to_dict())
    except HTTPException as e:
        logger.warning(f"User not found: {str(e)}")
        raise
    except ValueError:
        raise_http_exception(
            HTTP_400_BAD_REQUEST,
            f"Некорректный формат ID: {user_id}"
        )
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}", exc_info=True)
        raise


async def delete_user(user_id: str, user_repo: UserRepository) -> None:
    """Удаляет пользователя по ID."""
    try:
        UUID(user_id)
        user = await user_repo.get_one_or_none(id=user_id)
        if user is None:
            raise_http_exception(
                HTTP_404_NOT_FOUND,
                f"Пользователь с ID {user_id} не найден"
            )
        logger.info(f"Deleting user {user_id}")
        await user_repo.delete_where(User.id == user_id)
        await user_repo.session.commit()
        logger.info(f"User {user_id} deleted from repo")
    except HTTPException as e:
        logger.warning(f"User not found: {str(e)}")
        raise
    except ValueError:
        raise_http_exception(
            HTTP_400_BAD_REQUEST,
            f"Некорректный формат ID: {user_id}"
        )
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}", exc_info=True)
        raise
