from dataclasses import dataclass, field
from typing import Optional, ClassVar, List
import uuid
from datetime import datetime

@dataclass
class Task:
    title: str
    description: str = ""
    completed: bool = False
    project_id: Optional[str] = None
    _id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    # moving due_date here so it's not a dataclass field to prevent dataclass from trying to assign directly without validation
    _due_date: Optional[str] = field(default=None, init=False, repr=False)  # store as ISO date string
    
    # class-level collection
    all_tasks: ClassVar[List["Task"]] = []

    def __post_init__(self):       
        # register new task
        Task.all_tasks.append(self)

    @property
    def id(self) -> str:
        return self._id
    
    @id.setter
    def id(self, _):
        raise AttributeError("id is immutable")

    # Validated due_date property (YYYY-MM-DD format)
    @property
    def due_date(self) -> Optional[str]:
        return self._due_date

    @due_date.setter
    def due_date(self, value: Optional[str]):
        if value is not None:
            # Raises ValueError if not valid
            datetime.strptime(value, "%Y-%m-%d")
        self._due_date = value

    def set_due_date(self, due_date_str: str):
        # setting due_date with validation from property setter
        self.due_date = due_date_str
        
    def __str__(self):
        status = "✓" if self.completed else "•"
        return f"[{status}] {self.title}" + (f" (due {self.due_date})" if self.due_date else "")

    def mark_complete(self):
        """Mark this task as completed"""
        self.completed = True

    def mark_incomplete(self):
        """Mark this task as not completed"""
        self.completed = False

    @classmethod
    def get_all(cls) -> List["Task"]:
        """Return all Task instances"""
        return cls.all_tasks

    @classmethod
    def find_by_project(cls, project_id: str) -> List["Task"]:
        """Return all tasks belonging to a given project"""
        # list compression
        return [task for task in cls.all_tasks if task.project_id == project_id]
    
    @classmethod
    def clear_all(cls):
        """Reset the global tasks list (for testing purposes)"""
        cls.all_tasks.clear()