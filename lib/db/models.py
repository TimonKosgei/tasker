from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Relationship to Project (one-to-many)
    projects = relationship("Project", back_populates="user")

    def add_project(self, project):
        self.projects.append(project)


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

    def add_task(self, task):
        self.tasks.append(task)


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