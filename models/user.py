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
        """Add a project name (or later a Project object) to this user"""
        self.projects.append(project)

    def remove_project(self, project: str) -> bool:
        """Remove a project from this user's list if it exists"""
        if project in self.projects:
            self.projects.remove(project)
            return True
        return False
    
    def __str__(self) -> str:
        """
        Human-readable string for CLI printing.
        Example: "User: Alex (alex@example.com)"
        """
        return f"User: {self.name} ({self.email})"

    @classmethod
    def get_all(cls):
        """Return all User instances."""
        return cls.all_users
    
    @classmethod
    def find_by_email(cls, email: str) -> "User":
        """Search for the first user matching a given email; returns the User object if found, else None"""
        return next((u for u in cls.all_users if u.email == email), None)

    @classmethod
    def clear_all(cls):
        """Reset the global user list"""
        cls.all_users.clear()