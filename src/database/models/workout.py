from datetime import date
from sqlalchemy import ForeignKey, String, Date, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base

class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True, comment="Дата тренування")
    exercise_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    weight: Mapped[float] = mapped_column(Float, nullable=False, comment="Вага обтяження в кг")
    sets: Mapped[int] = mapped_column(Integer, nullable=False, comment="Кількість підходів")
    reps: Mapped[int] = mapped_column(Integer, nullable=False, comment="Кількість повторень")

    # Relationship back to User
    user: Mapped["User"] = relationship(back_populates="workout_logs")

    def __repr__(self) -> str:
        return f"<WorkoutLog user_id={self.user_id} ex={self.exercise_name} {self.sets}x{self.reps}>"