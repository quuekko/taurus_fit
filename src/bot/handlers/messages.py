from datetime import date
from aiogram import Router, F
from aiogram.types import Message

from src.services.ai_agent import SmartTrainerAgent
from src.database.repositories.user import UserRepository
from src.database.repositories.workout import WorkoutRepository
from src.database.repositories.nutrition import NutritionRepository
from src.database.models.workout import WorkoutLog
from src.database.models.nutrition import NutritionLog

router = Router(name="messages_router")
agent = SmartTrainerAgent()

@router.message(F.text)
async def handle_natural_language(
    message: Message, 
    user_repo: UserRepository,
    workout_repo: WorkoutRepository,
    nutrition_repo: NutritionRepository
):
    # 1. Перевіряємо, чи зареєстрований користувач
    user = await user_repo.get_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("Будь ласка, натисни /start для реєстрації.")
        return

    # 2. Показуємо статус "друкує...", поки ШІ думає
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # 3. Відправляємо текст в Gemini
    try:
        tool_calls = await agent.process_user_message(message.text)
    except Exception as e:
        await message.answer("Упс, сталася помилка при зверненні до мозку AI.")
        print(f"AI Error: {e}")
        return

    if not tool_calls:
        # Якщо модель не викликала інструменти (наприклад, це була просто розмова)
        await message.answer("Зрозумів! Якщо це було тренування чи їжа, спробуй написати конкретніше (наприклад: 'жим ногами 220 кг').")
        return

    response_messages = []
    today = date.today()

    # 4. Розбираємо JSON від ШІ та зберігаємо в БД
    for tool in tool_calls:
        args = tool["args"]
        
        if tool["name"] == "WorkoutTool":
            # Безпечно витягуємо значення, використовуючи .get() з дефолтними значеннями
            sets_val = args.get("sets", 1)
            reps_val = args.get("reps", 1)
            
            log = WorkoutLog(
                user_id=user.id,
                date=today,
                exercise_name=args["exercise_name"],
                weight=args["weight"],
                sets=sets_val,
                reps=reps_val
            )
            await workout_repo.add(log)
            response_messages.append(f"✅ {args['exercise_name']}: {args['weight']} кг ({sets_val}x{reps_val})")
            
        elif tool["name"] == "NutritionTool":
            log = NutritionLog(
                user_id=user.id,
                date=today,
                total_calories=args["total_calories"],
                protein=args.get("protein"),
                carbs=args.get("carbs"),
                fats=args.get("fats")
            )
            await nutrition_repo.add(log)
            response_messages.append(f"🍎 Харчування: {args['total_calories']} ккал")

        elif tool["name"] == "AnalyticsTool":
            days = args.get("days", 30)
            
            # 1. Дістаємо дані з бази
            workouts = await workout_repo.get_recent_workouts(user.id, days=days)
            
            if not workouts:
                response_messages.append(f"📊 За останні {days} днів тренувань не знайдено. Час іти в зал!")
                continue
                
            # 2. Форматуємо дані у текст для AI
            history_lines = [f"- {w.date}: {w.exercise_name} {w.weight}кг ({w.sets}x{w.reps})" for w in workouts]
            history_text = "\n".join(history_lines)
            
            # 3. Відправляємо дані в мозок для аналітики
            await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
            report = await agent.generate_analytics_report(user.goal, history_text)
            
            response_messages.append(f"📊 <b>Аналітика за {days} днів:</b>\n\n{report}")

    # 5. Відправляємо користувачу підтвердження
    final_text = "<b>Збережено в базу:</b>\n\n" + "\n".join(response_messages)
    await message.answer(final_text)