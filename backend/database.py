from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# --- 1. ІМПОРТУЄМО НАЛАШТУВАННЯ ---
from pydantic_settings import BaseSettings

# --- 2. СТВОРЮЄМО КЛАС ДЛЯ ЧИТАННЯ .env ---
class Settings(BaseSettings):
    # Ця змінна "автоматично" завантажить 
    # 'DATABASE_URL' з вашого файлу .env
    DATABASE_URL: str

    class Config:
        env_file = ".env"

# --- 3. СТВОРЮЄМО ЕКЗЕМПЛЯР НАЛАШТУВАНЬ ---
# Python прочитає .env та збереже DATABASE_URL тут
settings = Settings()

# --- 4. НАШ СТАРИЙ КОД, АЛЕ ТЕПЕР БЕЗПЕЧНИЙ ---
# Ми використовуємо 'settings.DATABASE_URL' (з .env)
# ЗАМІСТЬ "зашитого" рядка з паролем
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()