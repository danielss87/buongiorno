"""
Buongiorno API - ModelRun Model
Representa execuções do pipeline/modelo
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

try:
    from ..database import Base
except ImportError:
    from database import Base


class ModelRun(Base):
    """Modelo de Execução do Pipeline/Modelo"""

    __tablename__ = 'model_runs'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Run Info
    run_date = Column(DateTime, nullable=False, default=func.now(), index=True)
    status = Column(String(20), nullable=False, default='running')  # 'running', 'completed', 'failed'

    # Model Info
    model_name = Column(String(50), nullable=False)
    model_version = Column(String(20), nullable=True)

    # Metrics
    mae = Column(Float, nullable=True)
    rmse = Column(Float, nullable=True)
    mape = Column(Float, nullable=True)
    r2_score = Column(Float, nullable=True)

    # Dataset Info
    train_size = Column(Integer, nullable=True)
    test_size = Column(Integer, nullable=True)
    train_start_date = Column(DateTime, nullable=True)
    train_end_date = Column(DateTime, nullable=True)

    # Execution Info
    duration_seconds = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)

    # Hyperparameters and Config (stored as JSON)
    config = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    predictions = relationship("Prediction", back_populates="model_run")

    def __repr__(self):
        return f"<ModelRun(id={self.id}, model_name='{self.model_name}', status='{self.status}')>"

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'run_date': self.run_date.isoformat() if self.run_date else None,
            'status': self.status,
            'model_name': self.model_name,
            'model_version': self.model_version,
            'mae': self.mae,
            'rmse': self.rmse,
            'mape': self.mape,
            'r2_score': self.r2_score,
            'train_size': self.train_size,
            'test_size': self.test_size,
            'train_start_date': self.train_start_date.isoformat() if self.train_start_date else None,
            'train_end_date': self.train_end_date.isoformat() if self.train_end_date else None,
            'duration_seconds': self.duration_seconds,
            'error_message': self.error_message,
            'config': self.config,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
