from typing import Sequence
from fastapi import APIRouter, HTTPException, status


from app.crud import (
    create_accum_db,
    delete_accum_db,
    get_accum_by_name_db,
    get_accum_page_db,
    get_device_connected_accums_amount_db,
    is_device_exist_db,
    update_accum_db,
)
from app.model_data import (
    Accum,
    AccumCreate,
    AccumUpdate,
    AccumWithDevice,
    TupleAccums,
    Message,
)
from app.deps import CurrentAccumDep, SessionDep, get_device_db
from app.config import settings

app_accums = APIRouter(prefix="/accums")


@app_accums.get("/{accum_id}")
async def get_accum(current_accum: CurrentAccumDep) -> Accum:
    return Accum.model_validate(current_accum, from_attributes=True)


@app_accums.get("/accum_by_name/{accum_name}")
async def get_accum_by_name(session: SessionDep, accum_name: str) -> Accum:
    accum = await get_accum_by_name_db(session, accum_name)
    if accum is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accum with target name doesn't exist",
        )
    return Accum.model_validate(accum, from_attributes=True)


@app_accums.get("/")
async def get_accum_page(
    session: SessionDep, p: int = 1, p_size: int = 40
) -> Sequence[Accum]:
    accum_page_data = await get_accum_page_db(session, p, p_size)
    return TupleAccums.validate_python(accum_page_data, from_attributes=True)


# TODO: make bulk operation
@app_accums.get("/full/{accum_id}")
async def get_accum_with_device(
    session: SessionDep,
    current_accum: CurrentAccumDep,
) -> AccumWithDevice:
    """Get accum and connected device"""
    if current_accum.device_id is not None:
        accum_device = await get_device_db(session, current_accum.device_id)
    else:
        accum_device = None
    accum_with_device_data = {
        "accum": current_accum,
        "device": accum_device,
    }
    accum_with_device = AccumWithDevice.model_validate(
        accum_with_device_data, from_attributes=True
    )
    return accum_with_device


@app_accums.post("/add", status_code=status.HTTP_201_CREATED)
async def create_accum(session: SessionDep, accum_create: AccumCreate) -> Accum:
    if accum_create.device_id is not None:
        if not await is_device_exist_db(session, accum_create.device_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Accum try to point not exist device. accumulator.device_id doesn't exist",
            )
        target_device_conn_amount = await get_device_connected_accums_amount_db(
            session, accum_create.device_id
        )
        if target_device_conn_amount >= settings.DEVICE_MAX_CONNECTIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device already has max amount connections",
            )
    accum = await create_accum_db(session, accum_create)
    return Accum.model_validate(accum, from_attributes=True)


@app_accums.post("/update/{accum_id}")
async def update_accum(
    session: SessionDep, current_accum: CurrentAccumDep, accum_update: AccumUpdate
) -> Accum:
    if accum_update.device_id is not None:
        if not await is_device_exist_db(session, accum_update.device_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device with selected id (accumulator.device_id) doesn't exist",
            )
        target_device_conn_amount = await get_device_connected_accums_amount_db(
            session, accum_update.device_id
        )
        if target_device_conn_amount >= settings.DEVICE_MAX_CONNECTIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device already has max amount connections",
            )
    accum_updated = await update_accum_db(session, current_accum, accum_update)
    return Accum.model_validate(accum_updated, from_attributes=True)


@app_accums.post("/delete/{accum_id}")
async def delete_accum(session: SessionDep, current_accum: CurrentAccumDep) -> Message:
    await delete_accum_db(session, current_accum)
    return Message(message="Accumulator was successfully deleted")
