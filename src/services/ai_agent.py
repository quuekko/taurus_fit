from typing import List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

from src.config import settings
from src.schemas.ai_tools import WorkoutTool, NutritionTool, ProfileUpdateTool, AnalyticsTool

class SmartTrainerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0,
            api_key=settings.GEMINI_API_KEY
        )
        
        # Додали AnalyticsTool у список інструментів
        self.tools = [WorkoutTool, NutritionTool, ProfileUpdateTool, AnalyticsTool]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        self.system_prompt = SystemMessage(
            content=(
                "You are an elite AI fitness and body recomposition coach. "
                "Your job is to analyze the user's natural language messages and extract workout and nutrition data. "
                "If the user logs an exercise, call WorkoutTool. "
                "If the user logs food, call NutritionTool. "
                "If the user updates weight/height, call ProfileUpdateTool. "
                "If the user asks about their progress, history, or stats, call AnalyticsTool."
            )
        )

    async def process_user_message(self, text: str) -> List[Any]:
        prompt = ChatPromptTemplate.from_messages([
            self.system_prompt,
            ("human", "{input}")
        ])
        chain = prompt | self.llm_with_tools
        response = await chain.ainvoke({"input": text})
        return response.tool_calls

    async def generate_analytics_report(self, user_goal: str, workouts_text: str) -> str:
        """Другий виклик LLM: генерує текстовий звіт на основі сирих даних з БД."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "Ти професійний тренер. Проаналізуй історію тренувань користувача. "
             "Його ціль: {goal}. "
             "Зроби короткий висновок українською мовою: чи є прогрес у вагах, чи достатній об'єм. "
             "Напиши мотивуючий фідбек та 1-2 поради."
            ),
            ("human", "Ось мої тренування:\n{history}")
        ])
        
        # Для генерації тексту нам не потрібні Tools, викликаємо чисту модель (можна додати трохи креативності)
        text_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.4, 
            api_key=settings.GEMINI_API_KEY
        )
        
        chain = prompt | text_llm
        response = await chain.ainvoke({"goal": user_goal, "history": workouts_text})
        return response.content