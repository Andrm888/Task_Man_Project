from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List 
from contextlib import asynccontextmanager
#
# Импортируем наши модули напрямую
#

import schemas
import crud
from database import SessionLocal, engine, Base 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этот код выполнится ОДИН РАЗ при запуске сервера
    print("Сервер запускается, создаем таблицы...")
    Base.metadata.create_all(bind=engine)
    yield
    # Этот код выполнится при остановке сервера (нам не нужно)

app = FastAPI(lifespan=lifespan)

#
# "Зависимость" (Dependency)
#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Всегда закрываем сессию после запроса

#
# А теперь — наши API-Эндпоинты!
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

# -------------------------------------------------------------------
#  <<<<< НАЧАЛО НОВОГО КОДА >>>>>
# -------------------------------------------------------------------

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

# -------------------------------------------------------------------
#  <<<<< КОНЕЦ НОВОГО КОДА >>>>>
# -------------------------------------------------------------------

# --- 6. Наш старый корневой эндпоинт ---
@app.get("/")
def read_root():
    return {"message": "Привет! Сервер FastAPI работает!"}