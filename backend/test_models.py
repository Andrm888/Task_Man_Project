from sqlalchemy import create_engine, inspect
from database import Base
from models import Task  # noqa: F401

# --- 1. Настройка "фейковой" БД (в памяти) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# --- 2. НАШ ЮНИТ-ТЕСТ ДЛЯ МОДЕЛИ ---
def test_task_model_creates_table_correctly():
    """
    Этот тест проверяет, что модель Task(Base) 
    правильно создает таблицу 'tasks' со всеми 
    нужными колонками в "фейковой" БД.
    """
    
    Base.metadata.create_all(bind=engine)
    
    inspector = inspect(engine)
    
    # --- Шаг 3: Проверяем, что таблица 'tasks' существует ---
    table_names = inspector.get_table_names()
    print(f"Найденные таблицы в фейковой БД: {table_names}")
    
    assert "tasks" in table_names

    # --- Шаг 4: Проверяем, что ВСЕ колонки существуют ---
    columns = inspector.get_columns("tasks")
    
    # Создаем "set" (множество) имен колонок для 
    # удобной проверки
    column_names = {col['name'] for col in columns}
    
    print(f"Найденные колонки: {column_names}")
    
    assert "id" in column_names
    assert "title" in column_names
    assert "description" in column_names
    assert "status" in column_names

    # --- Шаг 5: (Опционально) Чистим за собой ---
    Base.metadata.drop_all(bind=engine)