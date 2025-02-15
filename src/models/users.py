from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(default=None, nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    age: Mapped[int]
    city: Mapped[str] = mapped_column(default=None, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(200))

    __table_args__ = (
        CheckConstraint("age > 0 AND age <= 150", name="users_age_check"),
    )
