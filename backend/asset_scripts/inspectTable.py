import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from database import db
from models import MatchesData
from sqlalchemy import inspect, text

print("🚀 Starting database inspection script...")

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Construct the correct path to the database file
db_path = os.path.join(basedir, '..', 'instance', 'ranklock.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print("📊 Initializing database connection...")
db.init_app(app)

if __name__ == "__main__":
    print("🔍 Entering application context...")
    
    try:
        with app.app_context():
            print("✅ Application context created successfully!")
            
            # DROP AND RECREATE TABLE
            print("🗑️ Dropping table if it exists...")
            with db.engine.connect() as conn:
                conn.execute(text("DROP TABLE IF EXISTS hero_stats;"))
                conn.commit()
            # Or drop all tables:
            # db.drop_all()
            
            print("🛠️ Creating fresh tables...")
            db.create_all()
            print("✅ Tables recreated!")
            
            # Check the new structure
            print("\n🔍 Inspecting new table structure...")
            inspector = inspect(db.engine)
            columns = inspector.get_columns('hero_stats')
            print("Columns in fresh 'hero_stats' table:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
                
            print("\n🎉 Table recreation completed!")
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

print("🏁 Script finished.")