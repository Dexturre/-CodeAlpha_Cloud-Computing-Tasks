from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

class DataEntry(Base):
    """Table for storing unique data entries"""
    __tablename__ = 'data_entries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_content = Column(Text, nullable=False)  # The actual data content
    data_type = Column(String(50), nullable=False)  # Type of data (text, number, mixed, etc.)
    content_hash = Column(String(64), nullable=False, unique=True)  # Hash of data for quick lookup
    similarity_score = Column(Float, default=0.0)  # Similarity score with existing data
    is_redundant = Column(Boolean, default=False)  # Whether this data is redundant
    is_false_positive = Column(Boolean, default=False)  # Whether this was a false positive
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_content_hash', 'content_hash'),
        Index('idx_data_type', 'data_type'),
        Index('idx_similarity_score', 'similarity_score'),
        Index('idx_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<DataEntry(id={self.id}, type={self.data_type}, redundant={self.is_redundant})>"

class ProcessingLog(Base):
    """Table for tracking data processing operations"""
    __tablename__ = 'processing_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    operation_type = Column(String(50), nullable=False)  # insert, update, delete, validate
    data_content = Column(Text, nullable=False)
    data_type = Column(String(50), nullable=False)
    content_hash = Column(String(64), nullable=False)
    similarity_score = Column(Float)
    is_redundant = Column(Boolean)
    is_false_positive = Column(Boolean)
    processing_time_ms = Column(Integer)  # Processing time in milliseconds
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    processed_at = Column(DateTime, default=func.now())
    
    # Indexes for analytics and debugging
    __table_args__ = (
        Index('idx_operation_type', 'operation_type'),
        Index('idx_processed_at', 'processed_at'),
        Index('idx_success', 'success'),
    )
    
    def __repr__(self):
        return f"<ProcessingLog(operation={self.operation_type}, success={self.success})>"

class SystemMetrics(Base):
    """Table for storing system performance metrics"""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(100), nullable=False)  # e.g., 'processing_time', 'redundancy_rate'
    metric_value = Column(Float, nullable=False)
    metric_timestamp = Column(DateTime, default=func.now())
    data_type = Column(String(50))  # Type of data this metric applies to
    
    # Index for time-series analysis
    __table_args__ = (
        Index('idx_metric_timestamp', 'metric_timestamp'),
        Index('idx_metric_name', 'metric_name'),
    )
    
    def __repr__(self):
        return f"<SystemMetric(name={self.metric_name}, value={self.metric_value})>"
