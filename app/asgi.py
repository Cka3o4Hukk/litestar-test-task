from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin

from app.config import settings
from app.routes import router


def create_app() -> Litestar:
    """Создаёт и настраивает приложение LiteStar."""

    # Конфигурарация OpenAPI для приложения
    openapi_config = OpenAPIConfig(
        title="Users API",
        version="1.0.0",
        path="/docs",
        root_schema_site="swagger"
    )

    # Подключение к базе данных
    db_config = SQLAlchemyAsyncConfig(
        connection_string=settings.database_url,
    )

    app = Litestar(
        route_handlers=[],
        plugins=[SQLAlchemyPlugin(config=db_config)],
        type_encoders={bytes: lambda b: b.decode()},
        openapi_config=openapi_config,
    )

    app.register(router)

    for route in app.routes:
        app.logger.info(f"Маршрут: {route.path} (методы: {route.methods})")

    return app


app = create_app()
