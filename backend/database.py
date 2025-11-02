from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. СТРОКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ
# Замените 'YOUR_PASSWORD' на пароль, который вы задали при установке PostgreSQL
DATABASE_URL = "postgresql://postgres:Fylhtq2004@localhost:5432/task_manager_db"

# 2. "ДВИЖОК" (ENGINE)
# Это основной "мост" SQLAlchemy к базе данных
engine = create_engine(DATABASE_URL)

# 3. "СОЗДАТЕЛЬ СЕССИЙ"
# Он будет создавать сессии (подключения) к БД для каждого запроса
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. "БАЗОВАЯ МОДЕЛЬ"
# Все наши классы-модели (например, Task) будут наследоваться от этого класса
Base = declarative_base()