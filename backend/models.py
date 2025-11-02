from sqlalchemy import Column, Integer, String
from database import Base # Импортируем 'Base' из нашего файла database.py

#
# Описываем нашу модель 'Task'
# SQLAlchemy будет использовать это для создания таблицы в БД
#
class Task(Base):
    __tablename__ = "tasks"  # Название таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, default="todo") # Например: "todo", "in_progress", "done"