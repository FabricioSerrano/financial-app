from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from financial_app.common.database import tables_registry

from .enums import UserRole


@tables_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, default=uuid4
    )
    name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    createdAt: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    role: Mapped[UserRole]
