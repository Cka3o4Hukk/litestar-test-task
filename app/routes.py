import logging
from litestar import Router
from litestar.di import Provide
from litestar.handlers.http_handlers import delete, get, post, put

from app.repository import provide_user_repo
from app.service import (
    create_user,
    list_users,
    get_user,
    update_user,
    delete_user
)


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

for route in router.routes:
    logger.info(f"Маршрут: {route.path} (методы: {route.methods})")
