import sys
from ranklock_app import create_app
from database import db
from sqlalchemy import inspect, text

app = create_app()

def reset_database():
    """Drops all tables and recreates them."""
    with app.app_context():
        print("Dropping all existing tables...")
        db.drop_all()
        print("Creating all tables from models...")
        db.create_all()
        print("Database has been reset successfully!")

def inspect_tables():
    """Inspects and prints the schema of all tables."""
    with app.app_context():
        print("\n Inspecting database schema...")
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        if not table_names:
            print("  - No tables found in the database.")
            return
            
        for table_name in table_names:
            print(f"\n--- Table: {table_name} ---")
            columns = inspector.get_columns(table_name)
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'reset':
            reset_database()
        elif command == 'inspect':
            inspect_tables()
        else:
            print(f"Unknown command: {command}. Use 'reset' or 'inspect'.")
    else:
        print("Please provide a command: 'reset' or 'inspect'.")