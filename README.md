# TaurusFIT 🐂 - AI-Powered Smart Trainer Telegram Bot

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://docs.aiogram.dev/en/latest/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-green.svg)](https://python.langchain.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)

TaurusFIT is an advanced, fully asynchronous Telegram bot designed to act as a personal fitness and body recomposition assistant. 

Instead of navigating complex menus or clicking buttons, users can simply send natural language messages (e.g., *"I benched 95kg for 5 reps today and ate 2500 kcal"*). The bot uses **LangChain** and **LLM Function Calling** to parse this text, extract entities, and store the structured data directly into a **PostgreSQL** database.

## 🚀 Key Features

* **Natural Language Processing:** Powered by the Gemini API, the bot understands free-text inputs for logging workouts, nutrition, and body metrics.
* **Smart Analytics:** Users can ask for progress reports (e.g., *"Show my stats for the last 7 days"*). The AI aggregates historical data from the database and generates personalized coaching feedback and advice.
* **Asynchronous Architecture:** Built with `aiogram 3` and `asyncpg` for non-blocking, high-performance execution.
* **Clean Architecture:** Implements the **Repository Pattern** to strictly isolate business/AI logic from database queries.

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Framework:** aiogram 3.x
* **AI & NLP:** LangChain, Google Gemini 2.5 Flash API (Function Calling)
* **Database:** PostgreSQL (Storage), Redis (FSM & Session Caching)
* **ORM & Migrations:** SQLAlchemy 2.0, Alembic
* **Infrastructure:** Docker, Docker Compose

## 📁 Project Structure

The project follows Domain-Driven Design (DDD) principles:

```text
src/
├── bot/               # Telegram UI layer (handlers, middlewares, keyboards)
├── database/          # Infra layer (Async engine, models, Repositories)
├── schemas/           # Pydantic v2 schemas (LLM Tools definitions)
├── services/          # Business logic (LangChain AI Agent integration)
└── main.py            # Entry point

```

## ⚙️ Installation & Setup

**1. Clone the repository**

```bash
git clone [https://github.com/quuekko/taurus-fit-bot.git](https://github.com/quuekko/taurus-fit-bot.git)
cd taurus-fit-bot

```

**2. Configure Environment Variables**
Create a `.env` file in the root directory and add your credentials:

```env
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_google_ai_studio_key

POSTGRES_USER=trainer_user
POSTGRES_PASSWORD=trainer_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=smart_trainer_db

REDIS_HOST=localhost
REDIS_PORT=6380

```

**3. Start the Infrastructure (Docker)**
Run PostgreSQL and Redis containers in the background:

```bash
docker-compose up -d

```

**4. Setup Python Environment & Dependencies**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```

**5. Apply Database Migrations**
Initialize the database tables using Alembic:

```bash
alembic upgrade head

```

**6. Run the Bot**

```bash
python -m src.main

```

## 🧠 How the AI Works Under the Hood

When a user sends a message, the following pipeline is executed:

1. **Middleware Intercept:** Opens an async DB session and initializes Data Repositories.
2. **Agent Processing:** The LangChain agent processes the text with the `SystemPrompt` and `Pydantic Tools`.
3. **Function Calling:** The LLM maps the text to specific tools (e.g., `WorkoutTool`, `NutritionTool`).
4. **Data Persistence:** The parsed JSON arguments are validated and passed to the specific Repository for database insertion.

## 👤 Author

**Dmytro Radkevych** * GitHub: [@quuekko](https://www.google.com/search?q=https://github.com/quuekko)

