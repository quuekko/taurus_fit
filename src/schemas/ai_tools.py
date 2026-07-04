from pydantic import BaseModel, Field

class WorkoutTool(BaseModel):
    """Call this tool when the user mentions performing an exercise, lifting weights, or doing sets/reps."""
    exercise_name: str = Field(..., description="The name of the exercise (e.g., 'Жим лежачи', 'Жим ногами', 'Присідання'). Translate to Ukrainian if needed.")
    weight: float = Field(..., description="The weight used for the exercise in kilograms (kg).")
    sets: int = Field(default=1, description="The number of sets performed. Default is 1 if not specified.")
    reps: int = Field(default=1, description="The number of repetitions performed. Default is 1 if not specified in the text.")

class NutritionTool(BaseModel):
    """Call this tool when the user mentions eating food, consuming calories, protein, carbs, or fats."""
    total_calories: int = Field(..., description="Total calories (kcal) consumed.")
    protein: float | None = Field(default=None, description="Amount of protein in grams, if mentioned.")
    carbs: float | None = Field(default=None, description="Amount of carbohydrates in grams, if mentioned.")
    fats: float | None = Field(default=None, description="Amount of fats in grams, if mentioned.")

class ProfileUpdateTool(BaseModel):
    """Call this tool when the user mentions their physical attributes like height, weight, or fitness goals."""
    height: float | None = Field(default=None, description="User's height in centimeters (cm).")
    current_weight: float | None = Field(default=None, description="User's current body weight in kilograms (kg).")

class AnalyticsTool(BaseModel):
    """Call this tool ONLY when the user asks for their progress, workout history, or statistics over a period of time."""
    days: int = Field(default=30, description="The number of days to analyze. Default is 30 if not specified (e.g., 'за місяць' = 30, 'за тиждень' = 7).")