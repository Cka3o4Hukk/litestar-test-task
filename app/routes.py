import logging
from litestar import Router
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.di import Provide
from litestar.handlers.http_handlers import delete, get, post, put
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """Репозиторий для работы с моделью User."""
    model_type = User


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """Предоставляет репозиторий для пользователей."""
    return UserRepository(session=db_session)


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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router(
    path="/users",
    dependencies={"user_repo": Provide(provide_user_repo)},
    route_handlers=[
        post("")(create_user),
        get("")(list_users),
        get("/{user_id:str}")(get_user),
        put("/{user_id:str}")(update_user),
        delete("/{user_id:str}")(delete_user),
    ],
)
