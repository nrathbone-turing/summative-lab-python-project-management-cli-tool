from dataclasses import dataclass, field
from typing import List, Optional, ClassVar
import uuid

@dataclass
class Project:
    id: str
    title: str
    description: str = ""
    due_date: Optional[str] = None  # ISO date string
    owner_user_id: Optional[str] = None
    tasks: List[str] = field(default_factory=list)
    _id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    
    # Class-level list to keep track of all projects
    all_projects: ClassVar[List["Project"]] = []

    def __post_init__(self):
        # register this instance
        Project.all_projects.append(self)

    def __str__(self):
        return f"Project({self.title})"

    def add_task(self, task: str):
        """Add a task to this project"""
        self.tasks.append(task)

    def remove_task(self, task: str):
        """Remove a task from this project if it exist; returns True if removed"""
        if task in self.tasks:
            self.tasks.remove(task)
            return True
        return False

    @classmethod
    def get_all(cls):
        """Return all project instances"""
        return cls.all_projects

    @classmethod
    def find_by_title(cls, title: str):
        """Find all projects matching the given title"""
        return [p for p in cls.all_projects if p.title == title]

    @classmethod
    def clear_all(cls):
        """Reset the global projects list (for testing purposes)"""
        cls.all_projects.clear()