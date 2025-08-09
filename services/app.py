from . import app as _   # makes package importable
from ..store.json_store import save_all, load_all
from ..models.user import User
from ..models.project import Project
from ..models.task import Task

class App:
    pass