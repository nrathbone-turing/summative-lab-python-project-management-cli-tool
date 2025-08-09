from dataclasses import dataclass, field
from typing import List, ClassVar
import uuid

@dataclass
class User:
    name: str
    email: str
    _id: str = field(default_factory=lambda: str(uuid.uuid4()))  # auto-generate UUID
    projects: List[str] = field(default_factory=list)

    # class-level collection
    all_users: ClassVar[List["User"]] = []

    def __post_init__(self):
        self._email = None
        # email validation
        self.email = self.email  
        # automatically register the new user
        User.all_users.append(self)

    @property
    def id(self): 
        """Read-only ID"""
        return self._id
    
    @id.setter
    def id(self, _): 
        raise AttributeError("id is immutable")

    @property
    def email(self): 
        return self._email
    
    @email.setter
    def email(self, value):
        if "@" not in value: 
            raise ValueError("invalid email")
        self._email = value

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
        """Human-readable string for CLI printing"""
        return f"User: {self.name} ({self.email})"

    @classmethod
    def get_all(cls):
        """Return all User instances"""
        return cls.all_users
    
    @classmethod
    def find_by_email(cls, email: str) -> "User":
        """Search for the first user matching a given email; returns the User object if found, else None"""
        return next((u for u in cls.all_users if u.email == email), None)

    @classmethod
    def clear_all(cls):
        """Reset the global user list"""
        cls.all_users.clear()