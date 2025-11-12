"""
Buongiorno API - Router de Previsões (Database Version)
Endpoints relacionados a previsões de preços
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

try:
    from ..database import get_db
    from ..services.prediction_service import PredictionService
    from ..repositories.asset_repository import AssetRepository
except ImportError:
    from database import get_db
    from services.prediction_service import PredictionService
    from repositories.asset_repository import AssetRepository


router = APIRouter()


@router.get("/predictions/latest")
def get_latest_prediction(
    asset: str = Query("gold", description="Ativo (gold, silver, oil)"),
    db: Session = Depends(get_db)
):
    """
    Retorna a última previsão disponível

    Args:
        asset: Código do ativo (gold, silver, oil)

    Returns:
        Dados da última previsão
    """
    try:
        service = PredictionService(db)
        prediction = service.get_latest_prediction(asset_code=asset)

        if not prediction:
            raise HTTPException(
                status_code=404,
                detail=f"Nenhuma previsão encontrada para o ativo '{asset}'"
            )

        return prediction

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/history")
def get_prediction_history(
    asset: str = Query("gold", description="Ativo"),
    limit: int = Query(30, description="Número de registros", ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retorna o histórico de previsões

    Args:
        asset: Código do ativo
        limit: Número máximo de registros

    Returns:
        Lista de previsões históricas
    """
    try:
        service = PredictionService(db)
        history = service.get_history(asset_code=asset, limit=limit)

        return {
            "asset": asset,
            "count": len(history),
            "predictions": history
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/history-errors")
def get_prediction_history_errors(
    asset: str = Query("gold", description="Ativo"),
    db: Session = Depends(get_db)
):
    """
    Retorna o histórico de previsões com erros calculados
    comparando com os valores reais

    Args:
        asset: Código do ativo

    Returns:
        Lista de previsões com erros de previsão calculados
    """
    try:
        service = PredictionService(db)
        history = service.get_history_with_errors(asset_code=asset)

        return {
            "asset": asset,
            "count": len(history),
            "predictions": history
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assets")
def list_assets(db: Session = Depends(get_db)):
    """
    Lista todos os ativos disponíveis

    Returns:
        Lista de ativos configurados
    """
    try:
        asset_repo = AssetRepository(db)
        assets = asset_repo.get_all()

        return {
            "assets": [asset.to_dict() for asset in assets]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
def list_models():
    """
    Lista todos os modelos disponíveis

    Returns:
        Lista de modelos configurados
    """
    models = [
        {
            "id": "arima",
            "name": "ARIMA",
            "description": "AutoRegressive Integrated Moving Average",
            "parameters": {
                "order": "(5,1,0)"
            },
            "active": True
        },
        {
            "id": "moving_average",
            "name": "Média Móvel",
            "description": "Média móvel simples",
            "parameters": {
                "window": 7
            },
            "active": True
        },
        {
            "id": "lstm",
            "name": "LSTM",
            "description": "Long Short-Term Memory Neural Network",
            "parameters": {},
            "active": False
        },
        {
            "id": "prophet",
            "name": "Prophet",
            "description": "Facebook Prophet",
            "parameters": {},
            "active": False
        }
    ]

    return {"models": models}
