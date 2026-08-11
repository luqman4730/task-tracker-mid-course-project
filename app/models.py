from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Normalize and check the title of a new task.

        Args:
            cls: The model class, supplied by Pydantic.
            v: The raw title from the input.

        Returns:
            str: The title with surrounding whitespace stripped. This stripped
                value is what gets stored.

        Raises:
            ValueError: If the title is empty after stripping, or if the
                stripped title is longer than 200 characters. Pydantic converts
                this into a ``ValidationError``, which FastAPI surfaces as an
                HTTP 422 response.
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError("title must not be blank")
        if len(stripped) > 200:
            raise ValueError("title must be at most 200 characters")
        return stripped


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Normalize and check the title supplied in a partial update.

        Pydantic only runs this validator when ``title`` is present in the
        input, so omitting the field entirely leaves the default of ``None``
        untouched. Passing ``title`` explicitly as ``null`` does run the
        validator and is rejected.

        Args:
            cls: The model class, supplied by Pydantic.
            v: The raw title from the input, which may be ``None`` when the
                caller passed an explicit null.

        Returns:
            Optional[str]: The title with surrounding whitespace stripped. The
                declared return type permits ``None``, but every ``None`` input
                raises before reaching the return.

        Raises:
            ValueError: If the title is ``None``, is empty after stripping, or
                is longer than 200 characters after stripping. Pydantic converts
                this into a ``ValidationError``, which FastAPI surfaces as an
                HTTP 422 response.
        """
        if v is None:
            raise ValueError("title must not be null")
        stripped = v.strip()
        if not stripped:
            raise ValueError("title must not be blank")
        if len(stripped) > 200:
            raise ValueError("title must be at most 200 characters")
        return stripped


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime
