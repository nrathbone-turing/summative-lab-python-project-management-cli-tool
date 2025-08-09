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

    # Class-level list to keep track of all projects
    all_projects: ClassVar[List["Project"]] = []

    def __post_init__(self):
        """Generate an ID if missing, then register this instance"""
        if not self.id:
            self.id = str(uuid.uuid4())
        Project.all_projects.append(self)

    def __str__(self):
        return f"Project({self.title})"

    def add_task(self, task: str):
        """Add a task to this project"""
        self.tasks.append(task)

    def remove_task(self, task: str):
        """Remove a task from this project if it exists"""
        if task in self.tasks:
            self.tasks.remove(task)

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