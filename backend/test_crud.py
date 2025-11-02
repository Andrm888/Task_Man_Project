import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Импортируем "чертежи" и "прораба"
import models
import schemas
from database import Base

# --- 1. Настройка "фейковой" БД (та же, что и раньше) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- 2. "Бригада по подготовке" (Фикстура для БД) ---
# Эта фикстура создает "фейковую" БД и таблицы ПЕРЕД тестом,
# и отдает ОДНУ сессию (db)
@pytest.fixture()
def db_session():
    # "Прораб" (Base) УЖЕ "знает" о 'models.Task',
    # потому что мы импортировали 'import models' вверху.
    
    # 1. "Строители" создают таблицу 'tasks'
    Base.metadata.create_all(bind=engine)
    
    # 2. Создаем "разговор" (сессию)
    db = TestingSessionLocal()
    try:
        # 3. "Отдаем" сессию тесту
        yield db
    finally:
        # 4. "Уборщики" закрывают сессию и сносят таблицу
        db.close()
        Base.metadata.drop_all(bind=engine)


# --- 3. НАШ UNIT-ТЕСТ ---
# Мы тестируем НЕ 'app', а 'crud.py' напрямую.
def test_crud_create_task(db_session):
    
    # Импортируем "рабочего" (CRUD) прямо здесь
    import crud
    
    # 1. Подготавливаем "материалы" (схему Pydantic)
    task_to_create = schemas.TaskCreate(
        title="Тест CRUD", 
        description="Проверка crud.py"
    )

    # 2. Вызываем "рабочего" (crud) напрямую
    db_task = crud.create_task(db=db_session, task=task_to_create)

    # 3. ПРОВЕРКА:
    # Убеждаемся, что "рабочий" вернул нам объект
    assert db_task is not None
    # Убеждаемся, что данные правильные
    assert db_task.title == "Тест CRUD"
    # Убеждаемся, что БД присвоила 'id'
    assert db_task.id is not None
    # Убеждаемся, что 'status' по умолчанию установлен
    assert db_task.status == "todo"

    # 4. Дополнительная проверка:
    # Запросим данные из БД еще раз, чтобы убедиться,
    # что они ТОЧНО сохранились
    saved_task = db_session.query(models.Task).get(db_task.id)
    assert saved_task is not None
    assert saved_task.title == "Тест CRUD"