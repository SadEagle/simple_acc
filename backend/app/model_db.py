from decimal import Decimal

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, MetaData, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs


# NOTE: Alembic naming constraints convention
# Ref: https://alembic.sqlalchemy.org/en/latest/naming.html#integration-of-naming-conventions-into-operations-autogenerate
# NOTE: AsyncAttr prevention implicit IO
# Ref: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class AccumDB(Base):
    __tablename__ = "accumulator"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    rated_voltage: Mapped[Decimal]
    residual_capacity: Mapped[Decimal]
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))
    device: Mapped["DeviceDB"] = relationship(back_populates="accums")

    __table_args__ = (
        CheckConstraint("voltage > 0"),
        CheckConstraint("residual_capacity > 0"),
    )


class DeviceDB(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    firmware_ver: Mapped[str]
    is_on: Mapped[bool]
    accums: Mapped[list[AccumDB]] = relationship(back_populates="device")
