# models/task.py
from dataclasses import dataclass, field
from typing import Optional, ClassVar, List
import uuid
from datetime import datetime

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    due_date: Optional[str] = None  # store as ISO date string
    completed: bool = False
    project_id: Optional[str] = None

    # class-level collection
    all_tasks: ClassVar[List["Task"]] = []

    def __post_init__(self):
        # auto-generate id if not provided
        if not self.id:
            self.id = str(uuid.uuid4())
        # register new task
        Task.all_tasks.append(self)

    def mark_complete(self):
        """Mark this task as completed"""
        self.completed = True

    def mark_incomplete(self):
        """Mark this task as not completed"""
        self.completed = False

    def set_due_date(self, due_date_str: str):
        """Set or update the due date (expects YYYY-MM-DD)."""
        try:
            datetime.strptime(due_date_str, "%Y-%m-%d")
            self.due_date = due_date_str
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format.")

    @classmethod
    def get_all(cls):
        """Return all Task instances"""
        return cls.all_tasks

    @classmethod
    def find_by_project(cls, project_id: str):
        """Return all tasks belonging to a given project"""
        # list compression
        return [task for task in cls.all_tasks if task.project_id == project_id]