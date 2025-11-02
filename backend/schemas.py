from pydantic import BaseModel

#
# 1. Базовая Схема (TaskBase)
# --------------------------
# Содержит общие поля, которые есть и при создании, и при чтении.
# Мы создаем ее, чтобы не дублировать код.
#
class TaskBase(BaseModel):
    title: str
    description: str | None = None  # Описание опционально, может быть None


#
# 2. Схема Создания (TaskCreate)
# ------------------------------
# Эту схему мы будем использовать, когда пользователь создает новую задачу.
# Она наследует все поля из TaskBase.
#
class TaskCreate(TaskBase):
    # При создании задачи пользователь не передает 'id' или 'status'.
    # 'id' создаст база данных.
    # 'status' будет 'todo' по умолчанию (как мы указали в models.py).
    pass


#
# 3. Схема Чтения (Task)
# ----------------------
# Эту схему мы будем использовать, когда отдаем данные о задаче пользователю.
#
class Task(TaskBase):
    id: int
    status: str

    # Эта "магическая" настройка говорит Pydantic
    # "Читай данные, даже если это не dict, а ORM-модель (объект SQLAlchemy)"
    # Это позволяет Pydantic "читать" данные из атрибутов объекта: task.id, task.title
    class Config:
        from_attributes = True  # (в Pydantic v1 это называлось orm_mode = True)

# 4. Схема Обновления (TaskUpdate)
# ------------------------------
# Эта схема будет использоваться при редактировании задачи.
# Все поля - необязательные (optional).
#
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None