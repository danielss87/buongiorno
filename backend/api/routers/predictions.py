"""
Buongiorno API - Router de Previsões
Endpoints relacionados a previsões de preços
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from services.prediction_service import PredictionService



router = APIRouter()

# Instância do serviço de previsões
prediction_service = PredictionService()


# TESTE: Endpoint de histórico com erros - movido para o INICIO para DEBUG
@router.get("/predictions/history-errors")
def get_prediction_history_errors(
    asset: str = Query("gold", description="Ativo")
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
        history = prediction_service.get_history_with_errors(asset=asset)

        return {
            "asset": asset,
            "count": len(history),
            "predictions": history
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Histórico não encontrado"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/latest")
def get_latest_prediction(asset: str = Query("gold", description="Ativo (gold, silver, oil)")):
    """
    Retorna a última previsão disponível
    
    Args:
        asset: Código do ativo (gold, silver, oil)
    
    Returns:
        Dados da última previsão
    """
    try:
        prediction = prediction_service.get_latest_prediction(asset=asset)
        
        if not prediction:
            raise HTTPException(
                status_code=404,
                detail=f"Nenhuma previsão encontrada para o ativo '{asset}'"
            )
        
        return prediction
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Arquivo de previsões não encontrado. Execute o pipeline primeiro."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/history")
def get_prediction_history(
    asset: str = Query("gold", description="Ativo"),
    limit: int = Query(30, description="Número de registros", ge=1, le=100)
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
        history = prediction_service.get_history(asset=asset, limit=limit)

        return {
            "asset": asset,
            "count": len(history),
            "predictions": history
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Histórico não encontrado"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/predictions/generate")
def generate_prediction(
    asset: str = Query("gold", description="Ativo"),
    model: str = Query("arima", description="Modelo (arima, moving_average)")
):
    """
    Gera uma nova previsão
    
    Args:
        asset: Código do ativo
        model: Modelo a ser usado
    
    Returns:
        Nova previsão gerada
    """
    try:
        # Por enquanto, retorna erro - implementar depois
        raise HTTPException(
            status_code=501,
            detail="Geração de previsões via API ainda não implementada. Use o pipeline Python."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assets")
def list_assets():
    """
    Lista todos os ativos disponíveis
    
    Returns:
        Lista de ativos configurados
    """
    assets = [
        {
            "id": "gold",
            "name": "Ouro",
            "symbol": "GC=F",
            "active": True,
            "description": "Contratos futuros de ouro (COMEX)"
        },
        {
            "id": "silver",
            "name": "Prata",
            "symbol": "SI=F",
            "active": False,
            "description": "Contratos futuros de prata (COMEX)"
        },
        {
            "id": "oil",
            "name": "Petróleo",
            "symbol": "CL=F",
            "active": False,
            "description": "Petróleo WTI (NYMEX)"
        }
    ]
    
    return {"assets": assets}


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
