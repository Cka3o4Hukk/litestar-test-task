from litestar import Litestar
from litestar.plugins.sqlalchemy import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from app.config import settings
from app.routes import router


def create_app() -> Litestar:
    """Создаёт и настраивает приложение LiteStar."""
    db_config = SQLAlchemyAsyncConfig(
        connection_string=settings.database_url,
    )
    return Litestar(
        route_handlers=[router],
        plugins=[SQLAlchemyPlugin(config=db_config)],
        type_encoders={bytes: lambda b: b.decode()},
    )


app = create_app()
