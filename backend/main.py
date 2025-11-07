from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List 

# --- НОВЫЙ ИМПОРТ ДЛЯ CORS ---
from fastapi.middleware.cors import CORSMiddleware

# --- ИМПОРТЫ ---
# (Мы НЕ импортируем 'models', 'engine' или 'Base', 
# т.к. 'main.py' их больше не использует)
import schemas
import crud
from database import SessionLocal

# -------------------------------------------------------------------
#  'create_all' и 'lifespan' здесь НЕТ.
#  Это "чистый" файл, безопасный для тестов 'pytest'.
# -------------------------------------------------------------------

app = FastAPI() # <-- "Чистый" FastAPI

# -------------------------------------------------------------------
#  ШАГ 1: ДОБАВЛЯЕМ "ПРОПУСК" (CORS)
#  (Чтобы "подружить" бэкенд и фронтенд)
# -------------------------------------------------------------------
origins = [
    "http://localhost:5173", # <-- "Адрес" вашего фронтенда (Vite/React)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # <-- Разрешить "друзей"
    allow_credentials=True,
    allow_methods=["*"],    # <-- Разрешить все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],    # <-- Разрешить все заголовки
)

#
# "Зависимость" (Dependency)
#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#
# А теперь — наши API-Эндпоинты! (ОНИ НЕ ИЗМЕНИЛИСЬ)
#

# --- 1. Эндпоинт для СОЗДАНИЯ ЗАДАЧИ ---
@app.post("/tasks/", response_model=schemas.Task)
def api_create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

# --- 2. Эндпоинт для ПОЛУЧЕНИЯ СПИСКА ЗАДАЧ ---
@app.get("/tasks/", response_model=List[schemas.Task]) 
def api_read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

# --- 3. Эндпоинт для ПОЛУЧЕНИЯ ОДНОЙ ЗАДАЧИ ---
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def api_read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# --- 4. Эндпоинт для ОБНОВЛЕНИЯ ЗАДАЧИ ---
@app.put("/tasks/{task_id}", response_model=schemas.Task)
def api_update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# --- 5. Эндпоинт для УДАЛЕНИЯ ЗАДАЧИ ---
@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def api_delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# --- 6. Наш старый корневой эндпоинт ---
@app.get("/")
def read_root():
    return {"message": "Привет! Сервер FastAPI работает!"}

