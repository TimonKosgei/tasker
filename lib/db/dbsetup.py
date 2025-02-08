from sqlalchemy import create_engine
from models import Base  

# Define the database URL
DATABASE_URL = "sqlite:///./app.db"  

# Create a new database engine
engine = create_engine(DATABASE_URL)

# Drop existing tables (optional, to reset everything)
Base.metadata.drop_all(engine)  # Deletes all tables

# Create new tables
Base.metadata.create_all(engine)  

print("Database reset and tables created successfully!")
