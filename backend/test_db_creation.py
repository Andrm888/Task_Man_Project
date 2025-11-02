from sqlalchemy import create_engine, inspect

# Импортируем 'Base' из нашего файла
from database import Base

# Настраиваем "фейковую" БД в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#
# Наш ОЧЕНЬ ПРОСТОЙ тест
#
def test_tasks_table_is_created():
    """
    Этот тест проверяет только ОДНУ вещь:
    Способна ли SQLAlchemy создать таблицу 'tasks' в 
    фейковой базе данных.
    Он не использует FastAPI или TestClient.
    """

    # --- Шаг 2: Даем команду "построить" таблицы ---
    Base.metadata.create_all(bind=engine)

    # --- Шаг 3: Проверка (Инспектор) ---
    # Создаем "инспектора", который "посмотрит" 
    # внутрь базы данных (engine)
    inspector = inspect(engine)

    # Получаем список всех таблиц, которые видит "инспектор"
    table_names = inspector.get_table_names()

    print(f"Найденные таблицы в фейковой БД: {table_names}")

    # --- Шаг 4: УТВЕРЖДЕНИЕ ---
    # Мы утверждаем, что в этом списке ЕСТЬ таблица 'tasks'
    assert "tasks" in table_names