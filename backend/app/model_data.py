from decimal import Decimal

from pydantic import BaseModel, Field


class AccumCreate(BaseModel):
    name: str
    rated_voltage: Decimal
    residual_capacity: Decimal
    device_id: int


class Accum(AccumCreate):
    id: int


class DeviceCreate(BaseModel):
    name: str
    firmware_ver: str
    is_on: bool


class Device(DeviceCreate):
    id: int
