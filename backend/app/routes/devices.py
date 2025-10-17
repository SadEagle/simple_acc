from fastapi import APIRouter, status

from app.crud import (
    create_device_db,
    delete_device_db,
    get_device_connected_accums_db,
    get_device_page_db,
    update_device_db,
)
from app.model_data import (
    Device,
    DeviceCreate,
    DeviceUpdate,
    DeviceWithAccums,
    # TupleDevices,
    Message,
)
from app.deps import CurrentDeviceDep, SessionDep


app_devices = APIRouter(prefix="/devices")


@app_devices.get("/{device_id}")
async def get_device(current_device: CurrentDeviceDep) -> Device:
    return Device.model_validate(current_device)


@app_devices.get("/{device_id}")
async def get_device_with_accums(
    session: SessionDep, current_device: CurrentDeviceDep
) -> DeviceWithAccums:
    accums_tuple = get_device_connected_accums_db(session, current_device.id)
    device_with_accums_data = {
        "device": current_device,
        "accums": accums_tuple,
    }
    device_with_accums = DeviceWithAccums.model_validate(
        device_with_accums_data, from_attributes=True
    )
    return device_with_accums


# @app_devices.get("/")
# async def get_device_page(
#     session: SessionDep, p: int = 1, p_size: int = 40
# ) -> tuple["Device", ...]:
#     device_page_data = await get_device_page_db(session, p, p_size)
#     return TupleDevices.validate_python(device_page_data, from_attributes=True)


@app_devices.post("/add", status_code=status.HTTP_201_CREATED)
async def create_device(session: SessionDep, device_create: DeviceCreate) -> Device:
    device = await create_device_db(session, device_create)
    return Device.model_validate(device, from_attributes=True)


@app_devices.post("/update/{device_id}")
async def update_device(
    session: SessionDep, current_device: CurrentDeviceDep, device_update: DeviceUpdate
) -> Device:
    device_updated = update_device_db(session, current_device, device_update)
    return Device.model_validate(device_updated, from_attributes=True)


@app_devices.post("/delete/{device_id}")
async def delete_device(
    session: SessionDep, current_device: CurrentDeviceDep
) -> Message:
    await delete_device_db(session, current_device)
    return Message(message="Device was successfully deleted")
