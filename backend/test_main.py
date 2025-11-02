import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Импортируем наше приложение и зависимость
from main import app, get_db
# Нам нужна Base из твоего файла database.py, чтобы создать таблицы
from database import Base 
# Нам нужны 'models', чтобы "зарегистрировать" таблицы в 'Base'
import models

# -------------------------------------------------------------------
# 1. НАСТРОЙКА ТЕСТОВОЙ БАЗЫ ДАННЫХ
# -------------------------------------------------------------------

# Используем SQLite в памяти для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Создаем тестовый "движок" (engine)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Создаем тестовую "фабрику сессий"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -------------------------------------------------------------------
# 2. ПОДМЕНА ЗАВИСИМОСТИ (Dependency Override)
# -------------------------------------------------------------------

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# -------------------------------------------------------------------
# 3. ФИКСТУРА Pytest (Наш Тестовый Клиент)
# -------------------------------------------------------------------

@pytest.fixture(scope="function")
def client():
    # Перед каждым тестом (scope="function"):
    # 1. "Регистрируем" модели (фикс)
    import models
    # 2. Создаем ВСЕ таблицы в нашей пустой БД в памяти
    Base.metadata.create_all(bind=engine)
    
    # 3. "yield" (возвращаем) клиента, чтобы тест мог его использовать
    with TestClient(app) as c:
        yield c
        
    # После каждого теста:
    # 4. Уничтожаем ВСЕ таблицы, чтобы следующий тест начал с чистого листа
    Base.metadata.drop_all(bind=engine)

# -------------------------------------------------------------------
# 4. НАШИ ТЕСТЫ
# -------------------------------------------------------------------

def test_read_root(client):
    """Тестируем корневой эндпоинт"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Привет! Сервер FastAPI работает!"}

def test_create_task(client):
    """Тестируем создание задачи"""
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    
    # --- ИСПРАВЛЕНО ---
    # Мы проверяем 'status', а не 'is_completed'
    assert data["status"] == "todo" 
    # --- КОНЕЦ ИСПРАВЛЕНИЯ ---
    
    assert "id" in data
    assert data["id"] == 1 

def test_read_tasks_empty(client):
    """Тестируем получение списка задач, когда он пуст"""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []

def test_read_tasks_with_data(client):
    """Тестируем получение списка задач, когда в нем есть данные"""
    # Сначала создадим пару задач
    client.post("/tasks/", json={"title": "Task 1", "description": "Desc 1"})
    client.post("/tasks/", json={"title": "Task 2", "description": "Desc 2"})
    
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_read_one_task(client):
    """Тестируем получение одной конкретной задачи"""
    # 1. Создаем задачу
    create_response = client.post(
        "/tasks/",
        json={"title": "Get Me", "description": "Find me"}
    )
    task_id = create_response.json()["id"]
    
    # 2. Получаем ее по ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Me"
    assert data["id"] == task_id

def test_read_one_task_not_found(client):
    """Тестируем получение задачи, которой не существует (404)"""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_update_task(client):
    """Тестируем обновление задачи"""
    # 1. Создаем задачу
    create_response = client.post(
        "/tasks/",
        json={"title": "Old Title", "description": "Old Desc"}
    )
    task_id = create_response.json()["id"]
    
    # 2. Обновляем ее
    # --- ИСПРАВЛЕНО ---
    # Мы отправляем 'status', а не 'is_completed'
    update_data = {
        "title": "New Title",
        "description": "New Desc",
        "status": "done" 
    }
    # --- КОНЕЦ ИСПРАВЛЕНИЯ ---
    
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["description"] == "New Desc"
    
    # --- ИСПРАВЛЕНО ---
    # Мы проверяем 'status'
    assert data["status"] == "done"
    # --- КОНЕЦ ИСПРАВЛЕНИЯ ---

def test_update_task_not_found(client):
    """Тестируем обновление задачи, которой не существует (404)"""
    response = client.put(
        "/tasks/999",
        json={"title": "New", "description": "New", "status": "done"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_task(client):
    """Тестируем удаление задачи"""
    # 1. Создаем задачу
    create_response = client.post(
        "/tasks/",
        json={"title": "To Be Deleted", "description": "Delete me"}
    )
    task_id = create_response.json()["id"]
    
    # 2. Удаляем ее
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    # Проверяем, что эндпоинт вернул удаленный объект
    assert delete_response.json()["title"] == "To Be Deleted" 
    
    # 3. Проверяем, что она действительно удалена (получаем 404)
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_delete_task_not_found(client):
    """Тестируем удаление задачи, которой не существует (404)"""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
