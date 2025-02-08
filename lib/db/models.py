from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

# Base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Relationship to Project (one-to-many)
    projects = relationship("Project", back_populates="user", cascade="all,delete")

    @validates('email')
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email format")  # Or a custom exception
        return email

    @validates('name')
    def validate_name(self, key, name):
      if not name: #check if the name is empty or contains only spaces
        raise ValueError("Name cannot be empty.")
      return name
    
class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relationship to User (many-to-one)
    user = relationship("User", back_populates="projects")

    # Relationship to Task (one-to-many)
    tasks = relationship("Task", back_populates="project", cascade="all, delete")
    #property methods
    @validates('status')
    def validate_status(self, key, status):
        allowed_statuses = ["not-started", "pending", "completed"]  # Define allowed statuses
        if status not in allowed_statuses:
            raise ValueError(f"Invalid status: {status}. Allowed statuses are: {allowed_statuses}")
        return status

    @validates('name')
    def validate_name(self, key, name):
      if not name: #check if the name is empty or contains only spaces
        raise ValueError("Name cannot be empty.")
      return name
    


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending")
    due_date = Column(Date)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    # Relationship to Project (many-to-one)
    project = relationship("Project", back_populates="tasks")

    #property methods
    @validates('status')
    def validate_status(self, key, status):
        allowed_statuses = ["not-started", "pending", "completed"]  # Define allowed statuses
        if status not in allowed_statuses:
            raise ValueError(f"Invalid status: {status}. Allowed statuses are: {allowed_statuses}")
        return status
    
    @validates('title')
    def validate_title(self, key, title):
      if not title: #check if the name is empty or contains only spaces
        raise ValueError("Title cannot be empty.")
      return title

    @validates('due_date')
    def validate_due_date(self, key, due_date):
        if due_date and due_date < date.today():
            raise ValueError("Due date cannot be in the past.")
        return due_date