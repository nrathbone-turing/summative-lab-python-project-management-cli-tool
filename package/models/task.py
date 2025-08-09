from dataclasses import dataclass

@dataclass
class Task:
    id: str
    title: str
    status: str = "todo"           # todo|in-progress|done
    assigned_to_user_id: str = ""
    project_id: str = ""