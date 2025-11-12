"""
Buongiorno API - Price Model
Representa preços históricos de ativos
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

try:
    from ..database import Base
except ImportError:
    from database import Base


class Price(Base):
    """Modelo de Preço Histórico"""

    __tablename__ = 'prices'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)

    # Price Data
    date = Column(Date, nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float)
    volume = Column(Float)

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    asset = relationship("Asset", back_populates="prices")

    # Composite Index for faster queries
    __table_args__ = (
        Index('idx_asset_date', 'asset_id', 'date'),
    )

    def __repr__(self):
        return f"<Price(asset_id={self.asset_id}, date={self.date}, close={self.close})>"

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'date': self.date.isoformat() if self.date else None,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'adj_close': self.adj_close,
            'volume': self.volume,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
