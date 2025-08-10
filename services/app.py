# services/app.py
from . import app as _   # makes package importable
from ..store.json_store import save_all, load_all
from ..models.user import User
from ..models.project import Project
from ..models.task import Task

class App:
    """Core application layer to coordinate users, projects, and tasks."""

    def save(self):
        """Save all models to persistent storage"""
        # Save using the current in-memory collections
        save_all(User.get_all(), Project.get_all(), Task.get_all())

    def load(self):
        """Load all models from persistent storage"""
        # Get raw dicts from JSON
        users_data, projects_data, tasks_data = load_all()

        # Clear existing collections before loading to avoid duplicates
        User.clear_all()
        Project.clear_all()
        Task.all_tasks.clear()

        # Rehydrate model objects from raw dictionaries
        for u in users_data:
            user_obj = User(name=u["name"], email=u["email"], projects=u.get("projects", []))
            user_obj._id = u.get("id", user_obj._id)  # fallback to generated if missing
        
        for p in projects_data:
            project_obj = Project(
                title=p["title"], 
                description=p.get("description", ""),
                due_date=p.get("due_date"), 
                owner_user_id=p.get("owner_user_id"), 
                tasks=p.get("tasks", [])
            )
            
            project_obj._id = p.get("id", project_obj._id)  # fallback to generated if missing
        
        for t in tasks_data:
            task_obj = Task(
                title=t["title"], 
                description=t.get("description", ""), 
                due_date=t.get("due_date"), 
                completed=t.get("completed", False), 
                project_id=t.get("project_id")
            )
            
            task_obj._id = t.get("id", task_obj._id)  # fallback to generated if missing