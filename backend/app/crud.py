from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.model_data import (
    AccumCreate,
    AccumUpdate,
    DeviceUpdate,
    DeviceCreate,
)
from app.model_db import AccumDB, DeviceDB


async def get_device_by_name_db(
    session: AsyncSession, device_name: str
) -> DeviceDB | None:
    statment = select(DeviceDB).where(DeviceDB.name == device_name)
    device = await session.scalar(statment)
    return device


async def get_accum_by_name_db(
    session: AsyncSession, accum_name: str
) -> AccumDB | None:
    statement = select(AccumDB).where(AccumDB.name == accum_name)
    accum = await session.scalar(statement)
    return accum


async def is_device_exist_db(session: AsyncSession, device_id: int) -> bool:
    return await session.get(DeviceDB, device_id) is not None


async def get_device_connected_accums_amount_db(
    session: AsyncSession, device_id: int
) -> int:
    statment = (
        select(func.count()).select_from(AccumDB).where(AccumDB.device_id == device_id)
    )
    connected_accum_amount = await session.scalar(statment)
    # .scalar() may be None, but count() always return value
    return connected_accum_amount or 0  # type: ignore


async def get_device_connected_accums_db(
    session: AsyncSession, device_id: int
) -> Sequence[AccumDB]:
    # TODO: may be good to make bulk select because may get big batch of data
    statment = select(AccumDB).where(AccumDB.device_id == device_id)
    connected_accums = (await session.scalars(statment)).all()
    return connected_accums


async def get_accum_page_db(
    session: AsyncSession, p: int, p_size: int
) -> Sequence[AccumDB]:
    statement = select(AccumDB).limit(p_size).offset((p - 1) * p_size)
    accum_page_data = (await session.scalars(statement)).all()
    return accum_page_data


async def create_accum_db(session: AsyncSession, accum_create: AccumCreate) -> AccumDB:
    accum_data = accum_create.model_dump()
    accum = AccumDB(**accum_data)
    session.add(accum)
    await session.commit()
    await session.refresh(accum)
    return accum


async def update_accum_db(
    session: AsyncSession, accum: AccumDB, accum_update: AccumUpdate
) -> AccumDB:
    accum_update_dict = accum_update.model_dump(exclude_unset=True)
    for key, value in accum_update_dict.items():
        setattr(accum, key, value)
    await session.commit()
    await session.refresh(accum)
    return accum


async def delete_accum_db(session: AsyncSession, accum: AccumDB) -> None:
    await session.delete(accum)
    await session.commit()


async def get_device_page_db(
    session: AsyncSession, p: int, p_size: int
) -> Sequence[DeviceDB]:
    statement = select(DeviceDB).limit(p_size).offset((p - 1) * p_size)
    device_page_data = (await session.scalars(statement)).all()
    return device_page_data


async def create_device_db(
    session: AsyncSession, device_create: DeviceCreate
) -> DeviceDB:
    device_data = device_create.model_dump()
    device = DeviceDB(**device_data)
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


async def update_device_db(
    session: AsyncSession, device: DeviceDB, device_update: DeviceUpdate
) -> DeviceDB:
    accum_update_dict = device_update.model_dump(exclude_unset=True)
    for key, value in accum_update_dict.items():
        setattr(device, key, value)
    await session.commit()
    await session.refresh(device)
    return device


async def delete_device_db(session: AsyncSession, device: DeviceDB) -> None:
    await session.delete(device)
    await session.commit()
