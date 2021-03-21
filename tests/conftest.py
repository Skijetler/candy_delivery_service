import os
import uuid
from types import SimpleNamespace

import pytest
from sqlalchemy_utils import create_database, drop_database
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from alembic.command import upgrade

from httpx import AsyncClient

from candy_delivery.api.app import create_app
from candy_delivery.api.__main__ import ENV_VAR_PREFIX
from candy_delivery.utils.db import DEFAULT_DB_URL, make_alembic_config


DB_URL = os.getenv("CI_" + ENV_VAR_PREFIX + "DB_URL", DEFAULT_DB_URL)


@pytest.fixture
def db():
    """
    Создает временную БД для запуска теста.
    """
    tmp_name = '.'.join([uuid.uuid4().hex, 'pytest'])
    tmp_url = DB_URL + tmp_name
    create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture()
def alembic_config(db):
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    cmd_options = SimpleNamespace(config='alembic.ini', name='alembic',
                                  db_url=db, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
async def migrated_db(alembic_config, db):
    """
    Возвращает URL к БД с примененными миграциями.
    """
    upgrade(alembic_config, 'head')
    return db

@pytest.fixture
def migrated_db_session(migrated_db):
    """
    Синхронное соединение со мигрированной БД.
    """
    engine = create_engine(migrated_db)
    conn = engine.connect()
    session = Session(conn)
    try:
        yield session
    finally:
        session.close()
        engine.dispose()

@pytest.fixture
async def api_client(migrated_db):
    """
    Создает объект для тестирования api
    """
    app = create_app(migrated_db)
    client = AsyncClient(app=app, base_url="http://test")
    
    try:
        yield client
    finally:
        await client.aclose()