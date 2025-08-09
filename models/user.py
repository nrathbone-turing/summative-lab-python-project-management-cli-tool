from dataclasses import dataclass, field
from typing import List, ClassVar

@dataclass
class User:
    id: str
    name: str
    email: str
    projects: List[str] = field(default_factory=list)

    # class-level collection
    all_users: ClassVar[List["User"]] = []

    def __post_init__(self):
        # automatically register the new user
        User.all_users.append(self)

    def add_project(self, project: str):
        """Add a project name (or later a Project object) to this user."""
        self.projects.append(project)

    @classmethod
    def get_all(cls):
        """Return all User instances."""
        return cls.all_users