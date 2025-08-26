from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base, DataEntry, ProcessingLog, SystemMetrics
from config import Config

class DatabaseManager:
    """Handles database operations for the Data Redundancy Removal System"""
    
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL, pool_size=Config.DATABASE_POOL_SIZE, max_overflow=Config.DATABASE_MAX_OVERFLOW)
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def add_data_entry(self, data_content, data_type, content_hash):
        """Add a new data entry to the database"""
        session = self.get_session()
        try:
            new_entry = DataEntry(data_content=data_content, data_type=data_type, content_hash=content_hash)
            session.add(new_entry)
            session.commit()
            # Refresh the object to ensure it's fully loaded
            session.refresh(new_entry)
            return new_entry
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error adding data entry: {e}")
            return None
        finally:
            session.close()
    
    def get_data_entry_by_hash(self, content_hash):
        """Retrieve a data entry by its content hash"""
        session = self.get_session()
        try:
            return session.query(DataEntry).filter_by(content_hash=content_hash).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving data entry: {e}")
            return None
        finally:
            session.close()
    
    def log_processing(self, operation_type, data_content, data_type, content_hash, similarity_score, is_redundant, is_false_positive):
        """Log a processing operation"""
        session = self.get_session()
        try:
            log_entry = ProcessingLog(
                operation_type=operation_type,
                data_content=data_content,
                data_type=data_type,
                content_hash=content_hash,
                similarity_score=similarity_score,
                is_redundant=is_redundant,
                is_false_positive=is_false_positive
            )
            session.add(log_entry)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error logging processing: {e}")
        finally:
            session.close()
    
    def get_all_data_entries(self):
        """Retrieve all data entries"""
        session = self.get_session()
        try:
            return session.query(DataEntry).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving all data entries: {e}")
            return []
        finally:
            session.close()
