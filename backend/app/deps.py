from typing import Annotated, AsyncGenerator, TypeAlias
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.model_db import AccumDB, DeviceDB
from app.db import async_engine


async def create_session() -> AsyncGenerator[AsyncSession]:
    # WARN: async expects no expiration
    # Ref: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    async with AsyncSession(async_engine, expire_on_commit=False) as async_session:
        yield async_session


SessionDep: TypeAlias = Annotated[AsyncSession, Depends(create_session)]


# NOTE: crud operator
async def get_accum_db(session: SessionDep, accum_id: int) -> AccumDB:
    statement = select(AccumDB).where(AccumDB.id == accum_id)
    session_accum = await session.scalar(statement)
    if session_accum is None:
        raise HTTPException(
            detail="Accumulator wasn't found", status_code=status.HTTP_404_NOT_FOUND
        )
    return session_accum


CurrentAccumDBDep: TypeAlias = Annotated[AsyncSession, Depends(get_accum_db)]


# NOTE: crud operator
async def get_device_db(session: SessionDep, device_id: int) -> AccumDB:
    statement = select(AccumDB).where(DeviceDB.id == device_id)
    session_accum = await session.scalar(statement)
    if session_accum is None:
        raise HTTPException(
            detail="Device wasn't found", status_code=status.HTTP_404_NOT_FOUND
        )
    return session_accum


CurrentDeviceDBDep: TypeAlias = Annotated[AsyncSession, Depends(get_device_db)]
