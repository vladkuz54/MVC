from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DB_LEVEL = "postgres"
DB_URL = f"postgresql+asyncpg://postgres:admin@localhost:5432/postgres"

engine = create_async_engine(DB_URL, echo=False)

Session = async_sessionmaker(engine)

Base = declarative_base()
