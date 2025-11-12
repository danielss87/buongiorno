"""
Buongiorno API - Serviço de Previsões (Database Version)
Lógica de negócio para gerenciar previsões usando banco de dados
"""

from typing import Dict, List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session

try:
    from ..repositories.asset_repository import AssetRepository
    from ..repositories.price_repository import PriceRepository
    from ..repositories.prediction_repository import PredictionRepository
except ImportError:
    from repositories.asset_repository import AssetRepository
    from repositories.price_repository import PriceRepository
    from repositories.prediction_repository import PredictionRepository


class PredictionService:
    """Serviço para gerenciar previsões de preços (usando Database)"""

    def __init__(self, db: Session):
        self.db = db
        self.asset_repo = AssetRepository(db)
        self.price_repo = PriceRepository(db)
        self.prediction_repo = PredictionRepository(db)

    def get_latest_prediction(self, asset_code: str = "gold") -> Optional[Dict]:
        """
        Retorna a última previsão disponível

        Args:
            asset_code: Código do ativo (gold, silver, oil)

        Returns:
            Dicionário com dados da previsão ou None
        """
        # Busca o asset
        asset = self.asset_repo.get_by_code(asset_code)
        if not asset:
            return None

        # Busca a última previsão (primeiro tenta futuras, depois qualquer uma)
        prediction = self.prediction_repo.get_latest_by_asset(asset.id, future_only=True)

        # Se não houver previsões futuras, busca a mais recente (fallback)
        if not prediction:
            prediction = self.prediction_repo.get_latest_by_asset(asset.id, future_only=False)

        if not prediction:
            return None

        # Formata datas
        target_date = prediction.target_date
        days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

        # Monta resposta
        return {
            "asset": asset_code,
            "prediction_date": prediction.prediction_date.isoformat(),
            "target_date": target_date.isoformat(),
            "target_day": days[target_date.weekday()],
            "current_price": prediction.current_price,
            "predicted_price": prediction.predicted_price,
            "change": prediction.change_abs,
            "change_pct": prediction.change_pct,
            "trend": prediction.trend,
            "model_used": prediction.model_used,
            "model_mape": prediction.model_mape,
            "model_accuracy": round(100 - prediction.model_mape, 2),
            "confidence": prediction.confidence
        }

    def get_history(self, asset_code: str = "gold", limit: int = 30) -> List[Dict]:
        """
        Retorna histórico de previsões

        Args:
            asset_code: Código do ativo
            limit: Número máximo de registros

        Returns:
            Lista de previsões
        """
        # Busca o asset
        asset = self.asset_repo.get_by_code(asset_code)
        if not asset:
            return []

        # Busca previsões
        predictions = self.prediction_repo.get_by_asset(asset.id, limit=limit)

        # Converte para lista de dicionários
        history = []
        for pred in predictions:
            history.append({
                "prediction_date": pred.prediction_date.isoformat(),
                "target_date": pred.target_date.isoformat(),
                "current_price": pred.current_price,
                "predicted_price": pred.predicted_price,
                "change": pred.change_abs,
                "change_pct": pred.change_pct,
                "trend": self._format_trend(pred.trend),
                "model_used": pred.model_used
            })

        return history

    def get_history_with_errors(self, asset_code: str = "gold") -> List[Dict]:
        """
        Retorna histórico de previsões com erros calculados

        Args:
            asset_code: Código do ativo

        Returns:
            Lista de previsões com erros calculados
        """
        # Busca o asset
        asset = self.asset_repo.get_by_code(asset_code)
        if not asset:
            return []

        # Busca todas as previsões
        predictions = self.prediction_repo.get_by_asset(asset.id)

        # Atualiza preços reais das previsões que ainda não têm
        self._update_real_prices(asset.id, predictions)

        # Converte para lista de dicionários
        history = []
        for pred in predictions:
            history.append({
                "prediction_date": pred.prediction_date.isoformat() if pred.prediction_date else None,
                "target_date": pred.target_date.isoformat(),
                "predicted_price": pred.predicted_price,
                "real_price": pred.real_price,
                "error_abs": round(pred.error_abs, 2) if pred.error_abs is not None else None,
                "error_pct": round(pred.error_pct, 2) if pred.error_pct is not None else None,
                "model_used": pred.model_used,
                "model_mape": pred.model_mape
            })

        return history

    def _update_real_prices(self, asset_id: int, predictions: List) -> None:
        """Atualiza preços reais das previsões que ainda não têm"""
        for pred in predictions:
            if pred.real_price is None:
                # Busca o preço real na data alvo
                real_price_record = self.price_repo.get_by_asset_and_date(asset_id, pred.target_date)

                if real_price_record:
                    # Atualiza a previsão com o preço real
                    self.prediction_repo.update_real_price(pred, real_price_record.close)

    def _format_trend(self, trend: str) -> str:
        """Formata o trend para exibição"""
        trend_map = {
            'up': 'ALTA ↗️',
            'down': 'BAIXA ↘️',
            'stable': 'ESTÁVEL →'
        }
        return trend_map.get(trend, trend)

    def create_prediction(self, asset_code: str, prediction_date: datetime,
                         target_date: date, current_price: float, predicted_price: float,
                         model_used: str, model_mape: float, model_run_id: int = None) -> Dict:
        """
        Cria uma nova previsão

        Args:
            asset_code: Código do ativo
            prediction_date: Data/hora da previsão
            target_date: Data alvo da previsão
            current_price: Preço atual
            predicted_price: Preço previsto
            model_used: Modelo usado
            model_mape: MAPE do modelo
            model_run_id: ID da execução do modelo

        Returns:
            Dicionário com a previsão criada
        """
        # Busca o asset
        asset = self.asset_repo.get_by_code(asset_code)
        if not asset:
            raise ValueError(f"Asset não encontrado: {asset_code}")

        # Calcula variações
        change_abs = predicted_price - current_price
        change_pct = (change_abs / current_price) * 100

        # Determina tendência
        if change_pct > 0.1:
            trend = 'up'
        elif change_pct < -0.1:
            trend = 'down'
        else:
            trend = 'stable'

        # Determina confiança baseada no MAPE
        if model_mape < 1:
            confidence = 'high'
        elif model_mape < 2:
            confidence = 'medium'
        else:
            confidence = 'low'

        # Cria a previsão
        prediction = self.prediction_repo.create(
            asset_id=asset.id,
            prediction_date=prediction_date,
            target_date=target_date,
            current_price=current_price,
            predicted_price=predicted_price,
            change_abs=change_abs,
            change_pct=change_pct,
            trend=trend,
            model_used=model_used,
            model_mape=model_mape,
            confidence=confidence,
            model_run_id=model_run_id
        )

        return prediction.to_dict()
