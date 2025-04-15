from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """Репозиторий для работы с моделью User."""
    model_type = User


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """Предоставляет репозиторий для пользователей."""
    return UserRepository(session=db_session)
