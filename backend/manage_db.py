#!/usr/bin/env python3
"""
Database management CLI for English Assistant
"""
import argparse
import logging
import sys
from pathlib import Path

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.database import DatabaseManager, create_tables, drop_tables
from utils.db_init import initialize_database, DatabaseSeeder
from utils.database import get_db_session

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_schema():
    """Create database schema"""
    try:
        create_tables()
        print("✅ Database schema created successfully")
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        sys.exit(1)


def drop_schema():
    """Drop database schema"""
    confirm = input("⚠️  This will delete all data. Are you sure? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled")
        return
    
    try:
        drop_tables()
        print("✅ Database schema dropped successfully")
    except Exception as e:
        print(f"❌ Error dropping schema: {e}")
        sys.exit(1)


def seed_data():
    """Seed database with initial data"""
    try:
        with get_db_session() as db:
            seeder = DatabaseSeeder()
            
            phrasal_verbs_count = seeder.seed_phrasal_verbs(db)
            history_count = seeder.seed_sample_history(db)
            
            print(f"✅ Database seeded successfully:")
            print(f"   - Phrasal verbs: {phrasal_verbs_count}")
            print(f"   - Sample history: {history_count}")
            
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        sys.exit(1)


def init_db():
    """Initialize complete database (schema + data)"""
    try:
        result = initialize_database()
        print(f"✅ Database initialized successfully: {result}")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)


def health_check():
    """Check database connection health"""
    try:
        if DatabaseManager.health_check():
            print("✅ Database connection is healthy")
            
            # Show connection info
            info = DatabaseManager.get_connection_info()
            print(f"   Connection info: {info}")
            
        else:
            print("❌ Database connection failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error checking database health: {e}")
        sys.exit(1)


def show_stats():
    """Show database statistics"""
    try:
        with get_db_session() as db:
            from models.database_models import History, PhrasalVerb
            
            # Count records
            history_count = db.query(History).count()
            phrasal_verbs_count = db.query(PhrasalVerb).count()
            
            # Count by difficulty
            beginner_count = db.query(PhrasalVerb).filter(PhrasalVerb.difficulty == 'beginner').count()
            intermediate_count = db.query(PhrasalVerb).filter(PhrasalVerb.difficulty == 'intermediate').count()
            advanced_count = db.query(PhrasalVerb).filter(PhrasalVerb.difficulty == 'advanced').count()
            
            # Count by status
            pending_count = db.query(PhrasalVerb).filter(PhrasalVerb.status == 'pending').count()
            in_progress_count = db.query(PhrasalVerb).filter(PhrasalVerb.status == 'in_progress').count()
            learned_count = db.query(PhrasalVerb).filter(PhrasalVerb.status == 'learned').count()
            
            print("📊 Database Statistics:")
            print(f"   History entries: {history_count}")
            print(f"   Phrasal verbs: {phrasal_verbs_count}")
            print(f"")
            print(f"   Difficulty levels:")
            print(f"     - Beginner: {beginner_count}")
            print(f"     - Intermediate: {intermediate_count}")
            print(f"     - Advanced: {advanced_count}")
            print(f"")
            print(f"   Learning status:")
            print(f"     - Pending: {pending_count}")
            print(f"     - In Progress: {in_progress_count}")
            print(f"     - Learned: {learned_count}")
            
    except Exception as e:
        print(f"❌ Error getting database statistics: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='English Assistant Database Management')
    parser.add_argument('command', choices=[
        'create', 'drop', 'seed', 'init', 'health', 'stats'
    ], help='Database command to execute')
    
    args = parser.parse_args()
    
    commands = {
        'create': create_schema,
        'drop': drop_schema,
        'seed': seed_data,
        'init': init_db,
        'health': health_check,
        'stats': show_stats
    }
    
    commands[args.command]()


if __name__ == "__main__":
    main()