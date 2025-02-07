from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime # For date objects

# Import your models (assuming they're in a file named models.py)
from models import User, Project, Task  # Adjust if your file name is different

# Database URL (replace with your actual database details)
DATABASE_URL = "sqlite:///./app.db"  # Example SQLite database

# Create the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
current_user  = None

def logout():
    global current_user
    current_user = None
    print("Logged out successfully.")


def login(session):
    view_users(session)
    global current_user
    try:
        user_id = input("Enter your user ID to login: ")
        user = session.query(User).filter_by(user_id=user_id).first()

        if user:
            print(f"Welcome, {user.name}!")
            current_user = user
        else:
            print("User not found. Please create an account or enter a valid ID.")
            return None  # Return None if login fails

    except Exception as e:
        print(f"Error during login: {e}")
        return None
def view_users(session):
    try:
        users = session.query(User).all()
        if users:
            print("Users found:")
            for user in users:
                print(f"ID: {user.user_id}, Name: {user.name}, Email: {user.email}")  # Customize output
        else:
            print("No users found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def add_project(session):
    try:
        if not current_user:
            print("kindly login first to continue")
            return 
        name = input("Enter project name:")
        description = input("Enter project description:")
        status = input("Enter the current status(not-started,pending,completed):")
        project = Project(name = name, description = description, status = status, user_id = current_user.user_id)
        session.add(project)
        session.commit()
        print(f"Project {name} created successfully!")
    except Exception as e:
        session.rollback()
        print(f"An error occured while adding a project: {e}")

def view_projects(session):
    user_id = current_user.user_id
    try:
        projects = session.query(Project).filter_by(user_id=user_id).all()
        if projects:
            print(f"Projects for user ID {user_id}:")
            for project in projects:
                print(f"ID: {project.project_id}, Name: {project.name}, Description: {project.description}, Status: {project.status}")
        else:
            print(f"No projects found for user ID {user_id}.")

    except Exception as e:
        print(f"Error viewing projects: {e}")

def view_tasks(session):
    try:
        user_id = current_user.user_id
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            print(f"Tasks for user ID {user_id}:")
            if user.projects:
                for project in user.projects:  
                    for task in project.tasks:  # Iterate through each project's tasks
                        print(f"Project: {project.name}, Task ID: {task.task_id}, Title: {task.title}, Description: {task.description}, Due Date: {task.due_date}, Status: {task.status}")
                        return True
            elif not user.projects:
                print(f"User {current_user.name} doesn't have any task!!")
                return None
        else:
            print(f"User with ID {user_id} not found.")

    except Exception as e:
        print(f"Error viewing tasks: {e}")

def update_task_status(session):
    try:
        check_tasks = view_tasks(session)
        if not check_tasks:
            return
        task_id = input("Enter the taskID of the task you want to update:")
        task = session.query(Task).filter_by(task_id=task_id).first()

        if task:
            new_status = input("Enter the new status (e.g., Pending, In Progress, Completed): ")
            task.status = new_status
            session.commit()
            print(f"Task status updated to {new_status}")
            return True  # Indicate success
        else:
            print(f"Task {task_id} not found.")
            return False  # Indicate failure

    except Exception as e:
        session.rollback()
        print(f"Error updating task status: {e}")
        return False
def delete_project(session):
    try:
        view_projects(session)
        project_id = input("Enter the project id of the project you want to delete:")
        project = session.query(Project).filter_by(project_id=project_id).first()

        if project:
            session.delete(project)  # Delete the project
            session.commit()
            print(f"Project {project_id} and its associated tasks deleted.")
            return True # Indicate successful deletion
        else:
            print(f"Project {project_id} not found.")
            return False # Indicate deletion failure

    except Exception as e:
        session.rollback()
        print(f"Error deleting project: {e}")
        return False

def update_project_status(session):
    try:
        view_projects(session)
        project_id = input("Enter the projectID that you want to update:")
        project = session.query(Project).filter_by(project_id=project_id).first()

        if project:
            new_status = input("Enter the new status (e.g., In Progress, Completed): ")
            project.status = new_status  # Update the project's status
            session.commit()
            print(f"Project status updated to {new_status}")
            return True  # Indicate success
        else:
            print(f"Project {project_id} not found.")
            return False  # Indicate failure

    except Exception as e:
        session.rollback()
        print(f"Error updating project status: {e}")
        return False
    

def add_task(session):
    try:
        print("\nAvailable Projects:")
        for project in current_user.projects:
            print(f"Project ID: {project.project_id}, Name: {project.name}")

        project_id = input("Enter the project id:")
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date_str = input("Enter the due date (YYYY-MM-DD): ")

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # Parse date string
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return None

        # Check if the project exists
        project = session.query(Project).filter_by(project_id=project_id).first()
        if not project:
            print(f"Project with ID {project_id} not found.")
            return None

        new_task = Task(title=title, description=description, due_date=due_date, project_id=project_id)
        session.add(new_task)
        session.commit()
        print(f"Task '{title}' added successfully with ID: {new_task.task_id}")
        return new_task

    except Exception as e:
        session.rollback()
        print(f"Error adding task: {e}")
        return None

def add_user(session):
    try:
        name = input("Enter user name: ")
        email = input("Enter user email: ")
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()

        print(f"User '{name}' added successfully with ID: {new_user.user_id}")
        return new_user  

    except Exception as e:
        session.rollback()  # Rollback on error
        print(f"An error occurred while adding user: {e}")
        return None  



# Example usage:
if __name__ == "__main__": 
    try: 
        session = Session()
        while True:
            print("\nTask Manager CLI")

            if current_user:  # Logged-in menu
                print("3. Logout")
                print("4. Create Project")
                print("5. Create Task")
                print("6. View Projects")
                print("7. View Tasks")
                print("8. Update Project Status")
                print("9. Delete Project")
                print("10. Update Task Status")
                print("11. Exit")
                available_choices = range(3, 12)

            else:  # Logged-out menu
                print("1. Create User")
                print("2. Login")
                print("12. View Users")
                print("11. Exit")
                available_choices = [1, 2, 12, 11]

            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice not in available_choices:
                print("Invalid choice! Try again.")
                continue

            if choice == 1:
                add_user(session)
            elif choice == 2:
                login(session)
            elif choice == 3 and current_user:
                logout()
            elif choice == 4 and current_user:
                add_project(session)
            elif choice == 5 and current_user:
                add_task(session)
            elif choice == 6 and current_user:
                view_projects(session)
            elif choice == 7 and current_user:
                view_tasks(session )
            elif choice == 8 and current_user:
                update_project_status(session)
            elif choice == 9 and current_user:
                delete_project(session)
            elif choice == 10 and current_user:
                update_task_status(session)
            elif choice == 12 and not current_user:
                view_users(session)
            elif choice == 11:
                print("Exiting Task Manager CLI...")
                break



    except Exception as e:
        print(f"A general occured: {e}")
    finally:
        session.close()

    