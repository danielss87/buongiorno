"""
Buongiorno API - Prediction Model
Representa previsões geradas pelos modelos
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

try:
    from ..database import Base
except ImportError:
    from database import Base


class Prediction(Base):
    """Modelo de Previsão"""

    __tablename__ = 'predictions'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    model_run_id = Column(Integer, ForeignKey('model_runs.id'), nullable=True)

    # Prediction Data
    prediction_date = Column(DateTime, nullable=False, index=True)  # Quando a previsão foi feita
    target_date = Column(Date, nullable=False, index=True)  # Data alvo da previsão

    # Prices
    current_price = Column(Float, nullable=False)  # Preço atual no momento da previsão
    predicted_price = Column(Float, nullable=False)  # Preço previsto
    real_price = Column(Float, nullable=True)  # Preço real observado (preenchido depois)

    # Changes
    change_abs = Column(Float, nullable=False)  # Variação absoluta esperada
    change_pct = Column(Float, nullable=False)  # Variação percentual esperada

    # Trend
    trend = Column(String(20), nullable=False)  # 'up', 'down', 'stable'

    # Model Info
    model_used = Column(String(50), nullable=False)  # 'arima', 'moving_average', etc
    model_mape = Column(Float, nullable=False)  # MAPE do modelo no momento da previsão
    confidence = Column(String(20), nullable=False)  # 'high', 'medium', 'low'

    # Error Metrics (calculados depois que temos real_price)
    error_abs = Column(Float, nullable=True)  # Erro absoluto
    error_pct = Column(Float, nullable=True)  # Erro percentual

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    asset = relationship("Asset", back_populates="predictions")
    model_run = relationship("ModelRun", back_populates="predictions")

    # Composite Indexes for faster queries
    __table_args__ = (
        Index('idx_asset_target_date', 'asset_id', 'target_date'),
        Index('idx_asset_prediction_date', 'asset_id', 'prediction_date'),
    )

    def __repr__(self):
        return f"<Prediction(asset_id={self.asset_id}, target_date={self.target_date}, predicted_price={self.predicted_price})>"

    def calculate_error(self):
        """Calcula o erro da previsão se temos o preço real"""
        if self.real_price is not None:
            self.error_abs = self.predicted_price - self.real_price
            self.error_pct = (self.error_abs / self.real_price) * 100

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'model_run_id': self.model_run_id,
            'prediction_date': self.prediction_date.isoformat() if self.prediction_date else None,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'current_price': self.current_price,
            'predicted_price': self.predicted_price,
            'real_price': self.real_price,
            'change_abs': self.change_abs,
            'change_pct': self.change_pct,
            'trend': self.trend,
            'model_used': self.model_used,
            'model_mape': self.model_mape,
            'confidence': self.confidence,
            'error_abs': self.error_abs,
            'error_pct': self.error_pct,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
