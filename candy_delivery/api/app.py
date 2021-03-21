from fastapi import FastAPI
from configargparse import Namespace
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.exceptions import RequestValidationError

from candy_delivery.api.routers import couriers, orders
from candy_delivery.api.validation_handler import RequestValidationHandler


def create_app(db_url) -> FastAPI:
    """
    Создает экземпляр приложения, готового к запуску.
    """

    app = FastAPI()
    app.add_middleware(DBSessionMiddleware, db_url=db_url, engine_args={"connect_args": {"options": "-c timezone=utc"}})
    app.add_exception_handler(RequestValidationError, handler=RequestValidationHandler)

    # Добавлени роутеров
    app.include_router(couriers.router,
                       prefix="/couriers",
                       tags=["courier"])
    app.include_router(orders.router,
                       prefix="/orders",
                       tags=["order"])

    return app