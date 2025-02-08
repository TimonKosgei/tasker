# Task Manager CLI

This project is a command-line interface (CLI) application for managing tasks. It allows users to create, organize, and track tasks associated with projects, all within a terminal environment. It uses SQLAlchemy to interact with a database.

## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Database Setup](#database-setup)

## Features

* **User Management:** Create, list, and view user accounts (name, email).
* **Project Management:** Create, list, update (status), and delete projects (name, description, status).
* **Task Management:** Create, list, and update (status) tasks (title, description, status, due date).
* **Task Association:** Tasks are associated with projects.
* **Data Persistence:** Uses SQLAlchemy to store data in a database (SQLite by default).
* **Login/Logout:** Securely login and logout of user accounts.
* **Interactive CLI:** Menu-driven interface for ease of use.

## Installation

### Prerequisites

* Python 3.8+
* `pipenv`: Install with `pip install pipenv`

### Installation Steps

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd tasker`  *(Make sure this directory name is correct)*
3. Install dependencies and create the virtual environment: `pipenv install`
4. Activate the virtual environment: `pipenv shell`

## Database Setup

1. **Database Initialization:** Navigate to the `lib/db` directory: `cd lib/db`
2. Run the database setup script: `python dbsetup.py` (This creates the database tables.)
3. (Optional) Add test data: `python seed.py` (This populates the database with sample data.)
4. Return to the main directory: `cd ..` (or `cd ../..` depending on your directory structure)

## Usage

The CLI application is accessed through the `cli.py` script.  Run it using: `python cli.py`

This will start the interactive menu. Here's how to use it:
**Logged in options**
1. View Projects
2. View Tasks
3. Create Project
4. Create Task
5. Update Project Status
6. Update Task Status
7. Get project info by id
8. Delete Project
9. Delete Task
10. Logout
11. Exit

**Logged out options**
1. Create User
2. Login
3. Get user info by id
4. View all users
5. Delete user
11. Exit