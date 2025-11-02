#
# Это одноразовый скрипт для создания 
# "настоящих" таблиц в "настоящей" (PostgreSQL) базе.
#
from database import engine, Base
import models  # noqa: F401

print("Подключаемся к PostgreSQL...")
print("Создаем таблицы (если их еще нет)...")

try:
    # "Прораб" (Base) "видит" 'models.Task' 
    # и создает таблицу 'tasks' в PostgreSQL
    Base.metadata.create_all(bind=engine)
    
    print("Готово! Таблицы успешно созданы в PostgreSQL.")
    
except Exception as e:
    print("\n--- ОШИБКА! ---")
    print("Не удалось создать таблицы. Проверьте 'DATABASE_URL' в database.py (особенно пароль!)")
    print(f"Ошибка: {e}")