import json
import os

TODOS_FILE = 'todos.json'

def load_tasks():
    """Loads tasks from the JSON file."""
    if not os.path.exists(TODOS_FILE):
        return []
    try:
        with open(TODOS_FILE, 'r') as file:
            tasks = json.load(file)
            # Ensure all tasks are dictionaries with expected keys
            for i, task in enumerate(tasks):
                if isinstance(task, str):
                    tasks[i] = {'description': task, 'completed': False}
                elif 'description' not in task:
                    # Handle malformed entry, perhaps by removing or fixing it
                    return [] # Or raise an error
            return tasks
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks):
    """Saves tasks to the JSON file."""
    with open(TODOS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, description):
    """Adds a new task to the list."""
    if description:
        tasks.append({'description': description, 'completed': False})
        save_tasks(tasks)
        print(f"Added task: '{description}'")
    else:
        print("Task description cannot be empty.")

def list_tasks(tasks):
    """Lists all tasks with their status."""
    if not tasks:
        print("No tasks to show.")
        return
    print("\n--- TODO List ---")
    for i, task in enumerate(tasks):
        status = "✓" if task.get('completed', False) else " "
        print(f"{i + 1}. [{status}] {task['description']}")
    print("-----------------\n")

def complete_task(tasks, task_index):
    """Marks a task as complete."""
    try:
        index = int(task_index) - 1
        if 0 <= index < len(tasks):
            if not tasks[index]['completed']:
                tasks[index]['completed'] = True
                save_tasks(tasks)
                print(f"Completed task: '{tasks[index]['description']}'")
            else:
                print("Task is already marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter the task number.")

def update_task(tasks, task_index, new_description):
    """Updates an existing task."""
    try:
        index = int(task_index) - 1
        if 0 <= index < len(tasks):
            if new_description:
                tasks[index]['description'] = new_description
                save_tasks(tasks)
                print(f"Updated task {task_index} to: '{new_description}'")
            else:
                print("New description cannot be empty.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter the task number.")

def print_help():
    """Prints the help menu."""
    print("\nAvailable commands:")
    print("  add <description>  - Add a new task")
    print("  list               - List all tasks")
    print("  complete <number>  - Mark a task as complete")
    print("  update <number> <new_description> - Update a task's description")
    print("  help               - Show this help message")
    print("  exit               - Exit the application")
    print()

def main():
    """Main application loop."""
    tasks = load_tasks()
    print("Welcome to your TODO list!")
    print_help()

    while True:
        command_input = input("> ").strip().split(maxsplit=1)
        command = command_input[0].lower() if command_input else ""
        
        if not command:
            continue

        arg = command_input[1] if len(command_input) > 1 else ""

        if command == 'add':
            add_task(tasks, arg)
        elif command == 'list':
            list_tasks(tasks)
        elif command == 'complete':
            complete_task(tasks, arg)
        elif command == 'update':
            update_args = arg.split(maxsplit=1)
            if len(update_args) == 2:
                task_index, new_description = update_args
                update_task(tasks, task_index, new_description)
            else:
                print("Usage: update <number> <new_description>")
        elif command == 'help':
            print_help()
        elif command == 'exit':
            print("Goodbye!")
            break
        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()
