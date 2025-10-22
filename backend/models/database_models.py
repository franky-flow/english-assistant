"""
SQLAlchemy database models for English Assistant
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY, JSON, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from backend.utils.database import Base


class History(Base):
    """Model for storing user interaction history"""
    
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, index=True)
    section = Column(String(50), nullable=False, index=True)
    query = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    examples = Column(ARRAY(Text), default=list)
    tags = Column(ARRAY(String), default=list, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Add constraint for valid sections
    __table_args__ = (
        CheckConstraint(
            section.in_(['vocabulary', 'correction', 'grammar', 'phrasal-verbs']),
            name='valid_section'
        ),
    )
    
    def __repr__(self):
        return f"<History(id={self.id}, section='{self.section}', query='{self.query[:50]}...')>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'section': self.section,
            'query': self.query,
            'result': self.result,
            'explanation': self.explanation,
            'examples': self.examples or [],
            'tags': self.tags or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class PhrasalVerb(Base):
    """Model for phrasal verbs with progress tracking"""
    
    __tablename__ = "phrasal_verbs"
    
    id = Column(Integer, primary_key=True, index=True)
    verb = Column(Text, nullable=False, unique=True, index=True)
    definition = Column(Text, nullable=False)
    examples = Column(ARRAY(Text), default=list)
    difficulty = Column(String(20), default='beginner', index=True)
    status = Column(String(20), default='pending', index=True)
    user_progress = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Add constraints for valid difficulty and status values
    __table_args__ = (
        CheckConstraint(
            difficulty.in_(['beginner', 'intermediate', 'advanced']),
            name='valid_difficulty'
        ),
        CheckConstraint(
            status.in_(['pending', 'in_progress', 'learned']),
            name='valid_status'
        ),
    )
    
    def __repr__(self):
        return f"<PhrasalVerb(id={self.id}, verb='{self.verb}', difficulty='{self.difficulty}', status='{self.status}')>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'verb': self.verb,
            'definition': self.definition,
            'examples': self.examples or [],
            'difficulty': self.difficulty,
            'status': self.status,
            'user_progress': self.user_progress or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_progress(self, progress_data: dict):
        """Update user progress for this phrasal verb"""
        if self.user_progress is None:
            self.user_progress = {}
        
        self.user_progress.update(progress_data)
        
        # Auto-update status based on progress
        if progress_data.get('completed', False):
            self.status = 'learned'
        elif progress_data.get('started', False):
            self.status = 'in_progress'