# app/service.py
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
    users = await user_repo.list()
    return [UserRead.model_validate(user) for user in users]


async def get_user(user_id: str, user_repo: UserRepository) -> UserRead:
    """Возвращает пользователя по ID."""
    user = await user_repo.get_one_or_none(id=user_id)
    if user is None:
        raise ValueError(f"Пользователь с ID {user_id} не найден")
    return UserRead.model_validate(user)


async def update_user(
    user_id: str,
    data: UserUpdate,
    user_repo: UserRepository,
) -> UserRead:
    """Обновляет пользователя по ID."""
    user = await user_repo.get_one_or_none(id=user_id)
    if user is None:
        raise ValueError(f"Пользователь с ID {user_id} не найден")
    user_dict = data.model_dump(exclude_unset=True)
    for key, value in user_dict.items():
        setattr(user, key, value)
    user = await user_repo.update(user)
    await user_repo.session.commit()
    return UserRead.model_validate(user)


async def delete_user(user_id: str, user_repo: UserRepository) -> None:
    """Удаляет пользователя по ID."""
    user = await user_repo.get_one_or_none(id=user_id)
    if user is None:
        raise ValueError(f"Пользователь с ID {user_id} не найден")
    await user_repo.delete(user)
    await user_repo.session.commit()
