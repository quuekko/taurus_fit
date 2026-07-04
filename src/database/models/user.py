import enum
from typing import List
from sqlalchemy import String, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base

class UserGoal(str, enum.Enum):
    RECOMPOSITION = "recomposition"
    CUT = "cut"
    BULK = "bulk"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    
    height: Mapped[float | None] = mapped_column(nullable=True)
    current_weight: Mapped[float | None] = mapped_column(nullable=True)
    
    goal: Mapped[UserGoal] = mapped_column(
        Enum(UserGoal), 
        default=UserGoal.RECOMPOSITION, 
        nullable=False
    )
    target_calories: Mapped[int | None] = mapped_column(nullable=True)

    # Relationships із каскадним видаленням
    workout_logs: Mapped[List["WorkoutLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    nutrition_logs: Mapped[List["NutritionLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User tg_id={self.telegram_id} goal={self.goal}>"