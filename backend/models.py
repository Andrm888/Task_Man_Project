import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqEnum
from sqlalchemy.sql import func
from database import Base

# 1. Створюємо Enum для статусів
# Це обмежує можливі значення трьома варіантами
class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    
    # 2. Використовуємо Enum замість простого String
    # native_enum=False зберігає це як текст у БД (простіше для сумісності),
    # але Python буде суворо перевіряти значення
    status = Column(SqEnum(TaskStatus, native_enum=False), default=TaskStatus.TODO)
    
    # 3. Додаємо часові мітки
    # server_default=func.now() -> БД сама поставить час при створенні
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # onupdate=func.now() -> БД сама оновить час при будь-якій зміні
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())