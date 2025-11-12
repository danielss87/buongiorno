"""
Buongiorno API - Price Repository
Data Access Layer para Prices
"""

from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

try:
    from ..models.price import Price
except ImportError:
    from models.price import Price


class PriceRepository:
    """Repository para gerenciar operações de Prices"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, asset_id: int, date: date, open: float, high: float,
               low: float, close: float, adj_close: float = None, volume: float = None) -> Price:
        """Cria um novo preço"""
        price = Price(
            asset_id=asset_id,
            date=date,
            open=open,
            high=high,
            low=low,
            close=close,
            adj_close=adj_close,
            volume=volume
        )
        self.db.add(price)
        self.db.commit()
        self.db.refresh(price)
        return price

    def bulk_create(self, prices: List[dict]) -> List[Price]:
        """Cria múltiplos preços de uma vez"""
        price_objects = [Price(**price_data) for price_data in prices]
        self.db.bulk_save_objects(price_objects, return_defaults=True)
        self.db.commit()
        return price_objects

    def get_by_id(self, price_id: int) -> Optional[Price]:
        """Busca preço por ID"""
        return self.db.query(Price).filter(Price.id == price_id).first()

    def get_by_asset_and_date(self, asset_id: int, date: date) -> Optional[Price]:
        """Busca preço específico por asset e data"""
        return self.db.query(Price).filter(
            and_(Price.asset_id == asset_id, Price.date == date)
        ).first()

    def get_by_asset(self, asset_id: int, limit: int = None, order_desc: bool = True) -> List[Price]:
        """Lista preços de um asset"""
        query = self.db.query(Price).filter(Price.asset_id == asset_id)

        if order_desc:
            query = query.order_by(desc(Price.date))
        else:
            query = query.order_by(Price.date)

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_by_date_range(self, asset_id: int, start_date: date, end_date: date) -> List[Price]:
        """Busca preços em um intervalo de datas"""
        return self.db.query(Price).filter(
            and_(
                Price.asset_id == asset_id,
                Price.date >= start_date,
                Price.date <= end_date
            )
        ).order_by(Price.date).all()

    def get_latest(self, asset_id: int) -> Optional[Price]:
        """Busca o preço mais recente de um asset"""
        return self.db.query(Price).filter(
            Price.asset_id == asset_id
        ).order_by(desc(Price.date)).first()

    def count_by_asset(self, asset_id: int) -> int:
        """Conta quantos preços existem para um asset"""
        return self.db.query(Price).filter(Price.asset_id == asset_id).count()

    def update(self, price: Price) -> Price:
        """Atualiza um preço"""
        self.db.commit()
        self.db.refresh(price)
        return price

    def upsert(self, asset_id: int, date: date, **price_data) -> Price:
        """Insere ou atualiza um preço"""
        existing = self.get_by_asset_and_date(asset_id, date)

        if existing:
            # Update
            for key, value in price_data.items():
                setattr(existing, key, value)
            return self.update(existing)
        else:
            # Insert
            return self.create(asset_id=asset_id, date=date, **price_data)

    def delete(self, price: Price) -> None:
        """Remove um preço"""
        self.db.delete(price)
        self.db.commit()

    def delete_by_asset(self, asset_id: int) -> int:
        """Remove todos os preços de um asset"""
        count = self.db.query(Price).filter(Price.asset_id == asset_id).delete()
        self.db.commit()
        return count
