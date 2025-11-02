from sqlalchemy.orm import Session

import models
import schemas

#
# 1. Функция для ПОЛУЧЕНИЯ ОДНОЙ задачи по ID
#
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

#
# 2. Функция для ПОЛУЧЕНИЯ СПИСКА всех задач
#
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

#
# 3. Функция для СОЗДАНИЯ новой задачи
#
def create_task(db: Session, task: schemas.TaskCreate):
    # 1. Создаем ОБЪЕКТ SQLAlchemy
    db_task = models.Task(**task.model_dump())

    # 2. Добавляем в сессию
    db.add(db_task)

    # 3. Сохраняем в БД
    db.commit()

    # 4. Обновляем объект (чтобы получить id)
    db.refresh(db_task)

    # 5. ВОЗВРАЩАЕМ созданный объект (ОБЯЗАТЕЛЬНО!)
    return db_task

#
# 4. Функция для ОБНОВЛЕНИЯ задачи
#
def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if db_task:
        update_data = task.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_task, key, value)
            
        db.commit()
        db.refresh(db_task)
        
    return db_task

#
# 5. Функция для УДАЛЕНИЯ задачи
#
def delete_task(db: Session, task_id: int):
    
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if db_task:
        db.delete(db_task)
        db.commit()
        
    return db_task