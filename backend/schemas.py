from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None  # Описание опционально, может быть None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    status: str

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None