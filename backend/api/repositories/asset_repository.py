"""
Buongiorno API - Asset Repository
Data Access Layer para Assets
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

try:
    from ..models.asset import Asset
except ImportError:
    from models.asset import Asset


class AssetRepository:
    """Repository para gerenciar operações de Assets"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, code: str, name: str, symbol: str, description: str = None, active: bool = True) -> Asset:
        """Cria um novo asset"""
        asset = Asset(
            code=code,
            name=name,
            symbol=symbol,
            description=description,
            active=active
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def get_by_id(self, asset_id: int) -> Optional[Asset]:
        """Busca asset por ID"""
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def get_by_code(self, code: str) -> Optional[Asset]:
        """Busca asset por código"""
        return self.db.query(Asset).filter(Asset.code == code).first()

    def get_all(self, active_only: bool = False) -> List[Asset]:
        """Lista todos os assets"""
        query = self.db.query(Asset)
        if active_only:
            query = query.filter(Asset.active == True)
        return query.all()

    def update(self, asset: Asset) -> Asset:
        """Atualiza um asset"""
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete(self, asset: Asset) -> None:
        """Remove um asset"""
        self.db.delete(asset)
        self.db.commit()

    def activate(self, asset: Asset) -> Asset:
        """Ativa um asset"""
        asset.active = True
        return self.update(asset)

    def deactivate(self, asset: Asset) -> Asset:
        """Desativa um asset"""
        asset.active = False
        return self.update(asset)
