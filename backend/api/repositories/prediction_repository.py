"""
Buongiorno API - Prediction Repository
Data Access Layer para Predictions
"""

from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

try:
    from ..models.prediction import Prediction
except ImportError:
    from models.prediction import Prediction


class PredictionRepository:
    """Repository para gerenciar operações de Predictions"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, asset_id: int, prediction_date: datetime, target_date: date,
               current_price: float, predicted_price: float, change_abs: float,
               change_pct: float, trend: str, model_used: str, model_mape: float,
               confidence: str, model_run_id: int = None, real_price: float = None) -> Prediction:
        """Cria uma nova previsão"""
        prediction = Prediction(
            asset_id=asset_id,
            model_run_id=model_run_id,
            prediction_date=prediction_date,
            target_date=target_date,
            current_price=current_price,
            predicted_price=predicted_price,
            real_price=real_price,
            change_abs=change_abs,
            change_pct=change_pct,
            trend=trend,
            model_used=model_used,
            model_mape=model_mape,
            confidence=confidence
        )

        # Calcula erro se temos real_price
        if real_price is not None:
            prediction.calculate_error()

        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def get_by_id(self, prediction_id: int) -> Optional[Prediction]:
        """Busca previsão por ID"""
        return self.db.query(Prediction).filter(Prediction.id == prediction_id).first()

    def get_latest_by_asset(self, asset_id: int, future_only: bool = True) -> Optional[Prediction]:
        """
        Busca a previsão mais recente de um asset

        Args:
            asset_id: ID do asset
            future_only: Se True, retorna apenas previsões futuras (target_date >= hoje)
        """
        query = self.db.query(Prediction).filter(Prediction.asset_id == asset_id)

        if future_only:
            today = date.today()
            query = query.filter(Prediction.target_date >= today)

        return query.order_by(desc(Prediction.prediction_date)).first()

    def get_by_asset(self, asset_id: int, limit: int = None) -> List[Prediction]:
        """Lista previsões de um asset"""
        query = self.db.query(Prediction).filter(
            Prediction.asset_id == asset_id
        ).order_by(desc(Prediction.target_date))

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_by_target_date(self, asset_id: int, target_date: date) -> List[Prediction]:
        """Busca todas as previsões para uma data alvo específica"""
        return self.db.query(Prediction).filter(
            and_(
                Prediction.asset_id == asset_id,
                Prediction.target_date == target_date
            )
        ).order_by(desc(Prediction.prediction_date)).all()

    def get_by_date_range(self, asset_id: int, start_date: date, end_date: date) -> List[Prediction]:
        """Busca previsões em um intervalo de datas"""
        return self.db.query(Prediction).filter(
            and_(
                Prediction.asset_id == asset_id,
                Prediction.target_date >= start_date,
                Prediction.target_date <= end_date
            )
        ).order_by(Prediction.target_date).all()

    def get_with_real_prices(self, asset_id: int) -> List[Prediction]:
        """Busca previsões que já têm preço real (para cálculo de erro)"""
        return self.db.query(Prediction).filter(
            and_(
                Prediction.asset_id == asset_id,
                Prediction.real_price.isnot(None)
            )
        ).order_by(Prediction.target_date).all()

    def get_without_real_prices(self, asset_id: int) -> List[Prediction]:
        """Busca previsões que ainda não têm preço real"""
        return self.db.query(Prediction).filter(
            and_(
                Prediction.asset_id == asset_id,
                Prediction.real_price.is_(None)
            )
        ).order_by(Prediction.target_date).all()

    def update_real_price(self, prediction: Prediction, real_price: float) -> Prediction:
        """Atualiza o preço real de uma previsão e recalcula erros"""
        prediction.real_price = real_price
        prediction.calculate_error()
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def update(self, prediction: Prediction) -> Prediction:
        """Atualiza uma previsão"""
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def delete(self, prediction: Prediction) -> None:
        """Remove uma previsão"""
        self.db.delete(prediction)
        self.db.commit()

    def count_by_asset(self, asset_id: int) -> int:
        """Conta quantas previsões existem para um asset"""
        return self.db.query(Prediction).filter(Prediction.asset_id == asset_id).count()
