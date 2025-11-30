from pydantic import BaseModel, ConfigDict
from datetime import datetime
# Импортируем наш Enum из models, чтобы использовать его в схемах
from models import TaskStatus

# 1. Базовая Схема (TaskBase)
# Содержит общие поля для создания и чтения
class TaskBase(BaseModel):
    title: str
    description: str | None = None

# 2. Схема Создания (TaskCreate)
# То, что мы ждем от пользователя при создании
class TaskCreate(TaskBase):
    pass

# 3. Схема Обновления (TaskUpdate)
# То, что мы ждем при обновлении (все поля опциональны)
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    # Теперь здесь используется наш Enum, а не просто строка
    status: TaskStatus | None = None

# 4. Схема Чтения (Task)
# То, что мы отдаем пользователю (включая ID и даты)
class Task(TaskBase):
    id: int
    status: TaskStatus
    # Новые поля с датами
    created_at: datetime
    updated_at: datetime | None = None

    # Настройка для работы с ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)