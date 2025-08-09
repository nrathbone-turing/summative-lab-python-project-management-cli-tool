import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from python_project_management_cli_tool.models.user import User


def test_user_creation():
    u = User("1", "Alex", "alex@example.com")
    assert u.id == "1"
    assert u.name == "Alex"
    assert u.email == "alex@example.com"
    assert u.projects == []
    assert u in User.get_all()

def test_add_project():
    u = User("2", "Jordan", "jordan@example.com")
    project = "DummyProject"
    u.add_project(project)
    assert project in u.projects
