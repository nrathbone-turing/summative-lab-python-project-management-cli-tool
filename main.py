import argparse

def add_user(args):
    print(f"Adding user: {args.name}")

def add_project(args):
    print(f"Adding project '{args.title}' for user: {args.user}")

def add_task(args):
    print(f"Adding task '{args.title}' to project: {args.project}")

# Wrap parser creation in a function so tests can import/build it cleanly
def build_parser():
    # Create the parser object and give the CLI a description
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    # Add subparsers to define separate commands
    # required=True here ensures argparse exits if no subcommand is given
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add-user commands
    user_parser = subparsers.add_parser("add-user", help="Add a new user")
    user_parser.add_argument("--name", required=True, help="Name of the user")
    user_parser.set_defaults(func=add_user)

    # add-project commands
    project_parser = subparsers.add_parser("add-project", help="Add a new project")
    project_parser.add_argument("--user", required=True, help="User for this project")
    project_parser.add_argument("--title", required=True, help="Title of the project")
    project_parser.set_defaults(func=add_project)

    # add-task commands
    task_parser = subparsers.add_parser("add-task", help="Add a new task")
    task_parser.add_argument("--project", required=True, help="Project to add the task to")
    task_parser.add_argument("--title", required=True, help="Title of the task")
    task_parser.set_defaults(func=add_task)

    return parser

# only parse/dispatch when run as a script (not on import)
if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()