"""
Database initialization and seeding utilities
"""
import logging
from typing import List, Dict, Any

from sqlalchemy.orm import Session

from backend.utils.database import get_db_session, DatabaseManager
from backend.models.database_models import History, PhrasalVerb

logger = logging.getLogger(__name__)


class DatabaseSeeder:
    """Utility class for seeding database with initial data"""
    
    @staticmethod
    def seed_phrasal_verbs(db: Session) -> int:
        """Seed database with initial phrasal verbs"""
        
        # Check if phrasal verbs already exist
        existing_count = db.query(PhrasalVerb).count()
        if existing_count > 0:
            logger.info(f"Phrasal verbs already exist ({existing_count} records). Skipping seeding.")
            return existing_count
        
        phrasal_verbs_data = [
            # Beginner level
            {
                'verb': 'get up',
                'definition': 'To rise from bed or a sitting position',
                'examples': ['I get up at 7 AM every day.', 'Please get up from the chair.'],
                'difficulty': 'beginner'
            },
            {
                'verb': 'sit down',
                'definition': 'To take a seat',
                'examples': ['Please sit down and relax.', 'She sat down at the table.'],
                'difficulty': 'beginner'
            },
            {
                'verb': 'turn on',
                'definition': 'To start or activate something',
                'examples': ['Turn on the lights, please.', 'Can you turn on the TV?'],
                'difficulty': 'beginner'
            },
            {
                'verb': 'turn off',
                'definition': 'To stop or deactivate something',
                'examples': ['Turn off the computer before leaving.', 'Don\'t forget to turn off the lights.'],
                'difficulty': 'beginner'
            },
            {
                'verb': 'look for',
                'definition': 'To search for something',
                'examples': ['I\'m looking for my keys.', 'She is looking for a new job.'],
                'difficulty': 'beginner'
            },
            
            # Intermediate level
            {
                'verb': 'give up',
                'definition': 'To stop trying or surrender',
                'examples': ['Don\'t give up on your dreams.', 'He gave up smoking last year.'],
                'difficulty': 'intermediate'
            },
            {
                'verb': 'look after',
                'definition': 'To take care of someone or something',
                'examples': ['Can you look after my cat while I\'m away?', 'She looks after her elderly parents.'],
                'difficulty': 'intermediate'
            },
            {
                'verb': 'run out of',
                'definition': 'To have no more of something',
                'examples': ['We ran out of milk.', 'I\'m running out of time.'],
                'difficulty': 'intermediate'
            },
            {
                'verb': 'figure out',
                'definition': 'To understand or solve',
                'examples': ['I can\'t figure out this math problem.', 'Did you figure out what went wrong?'],
                'difficulty': 'intermediate'
            },
            {
                'verb': 'break down',
                'definition': 'To stop working or collapse emotionally',
                'examples': ['My car broke down on the highway.', 'She broke down and started crying.'],
                'difficulty': 'intermediate'
            },
            
            # Advanced level
            {
                'verb': 'come across',
                'definition': 'To find by chance or seem to be',
                'examples': ['I came across an old photo yesterday.', 'She comes across as very confident.'],
                'difficulty': 'advanced'
            },
            {
                'verb': 'put up with',
                'definition': 'To tolerate or endure',
                'examples': ['I can\'t put up with this noise anymore.', 'She puts up with a lot from her boss.'],
                'difficulty': 'advanced'
            },
            {
                'verb': 'live up to',
                'definition': 'To meet expectations',
                'examples': ['The movie didn\'t live up to the hype.', 'He always lives up to his promises.'],
                'difficulty': 'advanced'
            },
            {
                'verb': 'stand up for',
                'definition': 'To defend or support',
                'examples': ['You should stand up for your beliefs.', 'She always stands up for her friends.'],
                'difficulty': 'advanced'
            },
            {
                'verb': 'keep up with',
                'definition': 'To stay at the same level or pace',
                'examples': ['It\'s hard to keep up with technology.', 'Can you keep up with the class?'],
                'difficulty': 'advanced'
            }
        ]
        
        created_count = 0
        for pv_data in phrasal_verbs_data:
            phrasal_verb = PhrasalVerb(**pv_data)
            db.add(phrasal_verb)
            created_count += 1
        
        db.commit()
        logger.info(f"Created {created_count} phrasal verbs")
        return created_count
    
    @staticmethod
    def seed_sample_history(db: Session) -> int:
        """Seed database with sample history entries"""
        
        # Check if history already exists
        existing_count = db.query(History).count()
        if existing_count > 0:
            logger.info(f"History entries already exist ({existing_count} records). Skipping seeding.")
            return existing_count
        
        sample_history = [
            {
                'section': 'vocabulary',
                'query': 'hello',
                'result': 'hola',
                'explanation': 'A common greeting used when meeting someone',
                'examples': ['Hello, how are you?', 'Hello there!'],
                'tags': ['greeting', 'basic']
            },
            {
                'section': 'vocabulary',
                'query': 'beautiful',
                'result': 'hermoso/hermosa',
                'explanation': 'Adjective describing something pleasing to look at',
                'examples': ['She is beautiful.', 'What a beautiful day!'],
                'tags': ['adjective', 'description']
            },
            {
                'section': 'grammar',
                'query': 'present simple vs present continuous',
                'result': 'Present simple is used for habits and facts, present continuous for actions happening now',
                'explanation': 'Present simple: I work every day. Present continuous: I am working now.',
                'examples': ['I eat breakfast every morning.', 'I am eating breakfast right now.'],
                'tags': ['grammar', 'tenses']
            },
            {
                'section': 'correction',
                'query': 'I am go to school',
                'result': 'I am going to school',
                'explanation': 'Use present continuous form "going" not base form "go"',
                'examples': ['I am going to the store.', 'She is going home.'],
                'tags': ['grammar', 'present-continuous']
            }
        ]
        
        created_count = 0
        for hist_data in sample_history:
            history = History(**hist_data)
            db.add(history)
            created_count += 1
        
        db.commit()
        logger.info(f"Created {created_count} sample history entries")
        return created_count


def initialize_database():
    """Initialize database with schema and seed data"""
    try:
        # Create tables
        DatabaseManager.initialize_database()
        
        # Seed initial data
        with get_db_session() as db:
            seeder = DatabaseSeeder()
            
            phrasal_verbs_count = seeder.seed_phrasal_verbs(db)
            history_count = seeder.seed_sample_history(db)
            
            logger.info(f"Database initialization complete:")
            logger.info(f"  - Phrasal verbs: {phrasal_verbs_count}")
            logger.info(f"  - Sample history: {history_count}")
            
            return {
                'phrasal_verbs': phrasal_verbs_count,
                'history': history_count
            }
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize database
    result = initialize_database()
    print(f"Database initialized successfully: {result}")