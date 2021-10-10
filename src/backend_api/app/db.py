from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager, asynccontextmanager
import env

Base = declarative_base()


def __get_endpoint():
    return f'{env.DB_USER}:{env.DB_PASS}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}'


def __get_engine(*, async_mode: bool = True, verbose: bool = False,
                 pytest: bool = env.PYTEST_MODE):
    '''
    Get new engine instance.
    Allow getting engine in sync mode, as that is better supported by FastAPI pytest
    '''
    kwargs = {'pool_size': env.DB_POOL_SIZE,
              'echo': verbose,
              'future': True}

    endpoint = __get_endpoint()

    if async_mode:
        return create_async_engine(
            f'postgresql+asyncpg://{endpoint}', **kwargs)
    else:
        kwargs.update({'executemany_mode': 'values_plus_batch'})
        return create_engine(
            f'postgresql+psycopg2://{endpoint}?client_encoding=utf8', **kwargs)


sync_engine = __get_engine(async_mode=False)
async_engine = __get_engine(async_mode=True)


def __get_session_class(*, async_mode: bool):
    'Get the session class, default to async mode'
    engine = async_engine if async_mode else sync_engine
    if async_mode:
        return sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession)
    else:
        return sessionmaker(bind=engine)


def sync_session():
    'Dependency for getting a db session'
    session_class = __get_session_class(async_mode=False)
    db = session_class()
    try:
        yield db
    finally:
        db.close()


async def async_session():
    'Dependency for getting a db session'
    session_class = __get_session_class(async_mode=True)
    db = session_class()
    try:
        yield db
    finally:
        await db.close()


@contextmanager
def sync_context():
    'Context manager for getting a db session'
    session_class = __get_session_class(async_mode=False)
    db = session_class()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def async_context():
    'Async context manager for getting a db session'
    session_class = __get_session_class(async_mode=True)
    db = session_class()
    try:
        yield db
    finally:
        await db.close()
