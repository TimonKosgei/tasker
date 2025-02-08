from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date  # For date objects

# Import your models (assuming they're in a file named models.py)
from models import User, Project, Task  # Adjust if your file name is different

# Database URL (replace with your actual database details)
DATABASE_URL = "sqlite:///./app.db"  # Example SQLite database

# Create the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Create Users
    user1 = User(name="Alice", email="alice@example.com")
    user2 = User(name="Bob", email="bob@example.com")
    user3 = User(name="Charlie", email="charlie@example.com")
    session.add_all([user1, user2, user3])
    session.commit()  # Commit the users first to generate IDs

    # Create Projects (associated with users)
    project1 = Project(name="Project A", description="Building a new website", user_id=user1.user_id)
    project2 = Project(name="Project B", description="Developing a mobile app", user_id=user2.user_id)
    project3 = Project(name="Project C", description="Marketing campaign", user_id=user1.user_id) # Alice has 2 projects
    session.add_all([project1, project2, project3])
    session.commit()  # Commit the projects to get their IDs

    # Create Tasks (associated with projects)
    task1 = Task(title="Design mockups", description="Create wireframes and visual designs", project_id=project1.project_id, due_date=date(2024, 1, 15))
    task2 = Task(title="Implement backend", description="Develop the server-side logic", project_id=project1.project_id, due_date=date(2024, 1, 22))
    task3 = Task(title="Frontend development", description="Build the user interface", project_id=project2.project_id, due_date=date(2024, 2, 1))
    task4 = Task(title="Social media ads", description="Run targeted ads on social platforms", project_id=project3.project_id, due_date=date(2023, 12, 20)) # Earlier due date
    task5 = Task(title="SEO optimization", description="Improve search engine ranking", project_id=project3.project_id, due_date=date(2024, 1, 5)) # Another task for project 3

    session.add_all([task1, task2, task3, task4, task5])
    session.commit()

    print("Seed data created successfully!")

except Exception as e:
    session.rollback()  # Rollback in case of error
    print(f"An error occurred: {e}")

finally:
    session.close()

