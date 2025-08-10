# store/json_store.py
import json, os

# Path to the database file — stored inside a "data" directory in the project root
DB_PATH = os.path.join("data", "db.json")

def _read():
    """
    Internal helper function to read data from the JSON file:
    - If the file doesn't exist, return empty lists for users, projects, and tasks
    - If the file exists but contains invalid JSON, also return empty lists
    """
    if not os.path.exists(DB_PATH):
        return {"users": [], "projects": [], "tasks": []}

    try:
        with open(DB_PATH, "r") as f:
            # Load and return parsed JSON
            return json.load(f)
    except json.JSONDecodeError:
        # If JSON file is corrupt or empty, return empty structure
        return {"users": [], "projects": [], "tasks": []}

def _write(data):
    """
    Write the given data dictionary to the JSON file & ensures the 'data' directory exists before writing.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Create folder if missing
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)  # Pretty-print JSON with 2-space indent (not specified, just my personal preference)

# Added helper to safely get an object's ID without triggering AttributeError
def _safe_get_id(obj):
    """Return _id if present, else id if present, else None"""
    if hasattr(obj, "_id"):
        return getattr(obj, "_id")
    if hasattr(obj, "id"):
        return getattr(obj, "id")
    return None

def save_all(users, projects, tasks):
    """
    Save all users, projects, and tasks to the JSON file; converts each object to a dictionary using __dict__ and ensures
    the 'id' field is included (falling back to '_id' if used internally)
    """
    _write({
        "users": [u.__dict__ | {"id": _safe_get_id(u)} for u in users],
        "projects": [p.__dict__ | {"id": _safe_get_id(p)} for p in projects],
        "tasks": [t.__dict__ | {"id": _safe_get_id(t)} for t in tasks],
    })

def load_all():
    """
    Load all users, projects, and tasks from the JSON file; returns them as three separate lists
    """
    data = _read()
    return data["users"], data["projects"], data["tasks"]