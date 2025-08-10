# scripts/seeded_data_demo.py
"""
Used for easier development to populate the database with sample users, projects, and tasks for demo purposes
Run (recommended from repo root): 
    python -m python_project_management_cli_tool.scripts.seeded_data_demo
or:
    python scripts/seeded_data_demo.py
"""

import sys
from pathlib import Path

# Add project root to path so imports work
sys.path.append(str(Path(__file__).resolve().parents[2]))

from python_project_management_cli_tool.models.user import User
from python_project_management_cli_tool.models.project import Project
from python_project_management_cli_tool.models.task import Task
from python_project_management_cli_tool.services.app import App

# Clear any existing in-memory data
User.clear_all()
Project.clear_all()
Task.clear_all()

# Create users
alice = User("Alice", "alice@example.com")
bob = User("Bob", "bob@example.com")

# Create projects
proj1 = Project(title="Website Redesign", description="Update homepage and navigation", owner_user_id=alice.id)
proj2 = Project(title="Marketing Campaign", description="Social media and email outreach", owner_user_id=bob.id)

# Assign projects to users
alice.projects.append(proj1.id)
bob.projects.append(proj2.id)

# Create tasks
Task(title="Draft wireframes", project_id=proj1.id)
Task(title="Review competitor sites", project_id=proj1.id)
Task(title="Design email template", project_id=proj2.id)
Task(title="Schedule social media posts", project_id=proj2.id, completed=True)

# Save everything
App().save()

print("Seed data created! You can now run the CLI to explore the sample data.")