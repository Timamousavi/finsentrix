import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from src.database.database import SessionLocal
from src.database.seed import seed_database, clear_database

def main():
    """Run database seeding."""
    db = SessionLocal()
    try:
        print("Clearing existing data...")
        clear_database(db)
        
        print("Seeding database with initial data...")
        seed_database(db)
        
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error during database seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 