import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import schemas
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_crud_create_task(db_session):
    
    import crud
    
    task_to_create = schemas.TaskCreate(
        title="Тест CRUD", 
        description="Проверка crud.py"
    )

    db_task = crud.create_task(db=db_session, task=task_to_create)

    assert db_task is not None
    assert db_task.title == "Тест CRUD"
    assert db_task.id is not None
    assert db_task.status == "todo"

    saved_task = db_session.query(models.Task).get(db_task.id)
    assert saved_task is not None
    assert saved_task.title == "Тест CRUD"