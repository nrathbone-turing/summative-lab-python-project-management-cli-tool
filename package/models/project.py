from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Project:
    id: str
    title: str
    description: str = ""
    due_date: Optional[str] = None  # ISO date string
    owner_user_id: Optional[str] = None
    tasks: List[str] = field(default_factory=list)
