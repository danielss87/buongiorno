"""
Buongiorno API - Asset Model
Representa ativos financeiros (ouro, prata, petróleo, etc)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

try:
    from ..database import Base
except ImportError:
    from database import Base


class Asset(Base):
    """Modelo de Ativo Financeiro"""

    __tablename__ = 'assets'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Asset Info
    code = Column(String(50), unique=True, nullable=False, index=True)  # 'gold', 'silver', 'oil'
    name = Column(String(100), nullable=False)  # 'Ouro', 'Prata', 'Petróleo'
    symbol = Column(String(20), nullable=False)  # 'GC=F', 'SI=F', 'CL=F'
    description = Column(String(500))

    # Status
    active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    prices = relationship("Price", back_populates="asset", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="asset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Asset(code='{self.code}', name='{self.name}', symbol='{self.symbol}')>"

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'symbol': self.symbol,
            'description': self.description,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
