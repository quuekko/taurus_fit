from datetime import date
from sqlalchemy import ForeignKey, Date, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base

class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True, comment="Дата прийому їжі / логування")
    
    total_calories: Mapped[int] = mapped_column(Integer, nullable=False, comment="Калорійність (ккал)")
    protein: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Білки (г)")
    carbs: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Вуглеводи (г)")
    fats: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Жири (г)")

    # Relationship back to User
    user: Mapped["User"] = relationship(back_populates="nutrition_logs")

    def __repr__(self) -> str:
        return f"<NutritionLog user_id={self.user_id} kcal={self.total_calories}>"