from http.client import HTTPException
import logging

from app.models import User
from app.repository import UserRepository
from app.schemas import UserCreate, UserRead, UserUpdate

logger = logging.getLogger(__name__)


async def create_user(data: UserCreate, user_repo: UserRepository) -> UserRead:
    """Создаёт нового пользователя."""
    try:
        logger.info(f"Input data: {data.model_dump()}")
        user_data = data.model_dump()
        user = User(**user_data)
        logger.info(f"Created User object: {user.__dict__}")
        user = await user_repo.add(user)
        user_id = str(user.id)
        logger.info(f"Added to repo: {user_id}")
        await user_repo.session.commit()
        logger.info(f"User created: {user_id}")
        user = await user_repo.get_one_or_none(id=user_id)
        if user is None:
            raise ValueError("User was not found after creation")
        user_dict = {
            "id": str(user.id),
            "name": user.name,
            "surname": user.surname,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        return UserRead.model_validate(user_dict)
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}", exc_info=True)
        raise


async def list_users(user_repo: UserRepository) -> list[UserRead]:
    """Возвращает список всех пользователей."""
    try:
        users = await user_repo.list()
        return [UserRead.model_validate(user.to_dict()) for user in users]
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}", exc_info=True)
        raise


async def get_user(user_id: str, user_repo: UserRepository) -> UserRead:
    """Возвращает пользователя по ID."""
    try:
        user = await user_repo.get_one_or_none(id=user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"Пользователь с ID {user_id} не найден"
            )
        return UserRead.model_validate(user.to_dict())
    except ValueError as e:
        logger.error(f"User not found: {str(e)}")
        raise
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
        user = await user_repo.get_one_or_none(id=user_id)
        if user is None:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        user_dict = data.model_dump(exclude_unset=True)
        logger.info(f"Updating user {user_id} with data: {user_dict}")
        for key, value in user_dict.items():
            if value is not None:
                setattr(user, key, value)
        user = await user_repo.update(user)
        await user_repo.session.commit()
        await user_repo.session.refresh(user)
        logger.info(f"User updated: {user.to_dict()}")
        return UserRead.model_validate(user.to_dict())
    except ValueError as e:
        logger.error(f"User not found: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}", exc_info=True)
        raise


async def delete_user(user_id: str, user_repo: UserRepository) -> None:
    """Удаляет пользователя по ID."""
    try:
        user = await user_repo.get_one_or_none(id=user_id)
        if user is None:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        logger.info(f"Deleting user {user_id}")
        await user_repo.delete_where(User.id == user_id)
        logger.info(f"User {user_id} deleted from repo")
        await user_repo.session.commit()
        logger.info(f"Deletion committed for user {user_id}")
    except ValueError as e:
        logger.error(f"User not found: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}", exc_info=True)
        raise
