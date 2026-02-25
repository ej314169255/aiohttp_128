import datetime
import os

from sqlalchemy import DateTime, Integer, String, func, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

POSTGRES_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_async_engine(POSTGRES_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {"id": self.id}


class Adv(Base):
    __tablename__= "records"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    # adv_id: MappedColumn[int] = mapped_column(Integer, ForeignKey("users.id"))
    owner: MappedColumn[str] = mapped_column(String)
    title: MappedColumn[str] = mapped_column(String)
    descr: MappedColumn[str] = mapped_column(String)
    status: MappedColumn[str] = mapped_column(String)
    registration_time: MappedColumn[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
        )

    def dict(self):
        return {
            "id": self.id,
            "owner": self.owner,
            "descr": self.descr,
            "registration_time": int(self.registration_time.timestamp()),
        }



class User(Base):

    __tablename__ = "users"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    name: MappedColumn[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: MappedColumn[str] = mapped_column(String(70), nullable=False)
    token: MappedColumn[str] = mapped_column(String, unique=True)
    registration_time: MappedColumn[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": int(self.registration_time.timestamp()),
        }

class Token(Base):
    __tablename__="tokens"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    token: MappedColumn[str] = mapped_column(String, unique=True)
    registration_time: MappedColumn[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    token_id: MappedColumn[int] = mapped_column(Integer, ForeignKey("users.id"))
    #user: MappedColumn[User] = relationship(User, back_populates="token", lazy="joined")

    
async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
