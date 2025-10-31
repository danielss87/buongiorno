"""
Buongiorno API - Serviço de Previsões
Lógica de negócio para gerenciar previsões
"""

import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Optional


class PredictionService:
    """Serviço para gerenciar previsões de preços"""
    
    def __init__(self):
        # Caminho relativo para os dados do pipeline
        self.base_path = os.path.join(
            os.path.dirname(__file__),
            '../../pipeline/data'
        )
    
    def get_latest_prediction(self, asset: str = "gold") -> Optional[Dict]:
        """
        Retorna a última previsão disponível
        
        Args:
            asset: Código do ativo
        
        Returns:
            Dicionário com dados da previsão ou None
        """
        try:
            # Por enquanto, suporta apenas gold
            # Depois pode adicionar lógica para outros ativos
            csv_path = os.path.join(
                self.base_path,
                'predictions',
                'predictions_history.csv'
            )
            
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")
            
            # Lê o CSV
            df = pd.read_csv(csv_path)
            
            if df.empty:
                return None
            
            # Pega a última linha
            latest = df.iloc[-1]
            
            # Formata datas
            target_date = pd.to_datetime(latest['target_date'])
            days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
            
            # Determina tendência
            trend_text = str(latest['trend']).lower()
            if 'alta' in trend_text:
                trend = 'up'
            elif 'baixa' in trend_text:
                trend = 'down'
            else:
                trend = 'stable'
            
            # Calcula confiança baseada no MAPE
            model_mape = float(latest['model_mape'])
            if model_mape < 1:
                confidence = 'high'
            elif model_mape < 2:
                confidence = 'medium'
            else:
                confidence = 'low'
            
            # Monta resposta
            prediction = {
                "asset": asset,
                "prediction_date": latest['prediction_date'],
                "target_date": latest['target_date'],
                "target_day": days[target_date.dayofweek],
                "current_price": float(latest['current_price']),
                "predicted_price": float(latest['predicted_price']),
                "change": float(latest['change_abs']),
                "change_pct": float(latest['change_pct']),
                "trend": trend,
                "model_used": latest['model_used'],
                "model_mape": model_mape,
                "model_accuracy": round(100 - model_mape, 2),
                "confidence": confidence
            }
            
            return prediction
        
        except Exception as e:
            raise Exception(f"Erro ao buscar previsão: {str(e)}")
    
    def get_history(self, asset: str = "gold", limit: int = 30) -> List[Dict]:
        """
        Retorna histórico de previsões
        
        Args:
            asset: Código do ativo
            limit: Número máximo de registros
        
        Returns:
            Lista de previsões
        """
        try:
            csv_path = os.path.join(
                self.base_path,
                'predictions',
                'predictions_history.csv'
            )
            
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")
            
            # Lê o CSV
            df = pd.read_csv(csv_path)
            
            # Pega os últimos N registros
            df = df.tail(limit)
            
            # Converte para lista de dicionários
            history = []
            for _, row in df.iterrows():
                history.append({
                    "prediction_date": row['prediction_date'],
                    "target_date": row['target_date'],
                    "current_price": float(row['current_price']),
                    "predicted_price": float(row['predicted_price']),
                    "change": float(row['change_abs']),
                    "change_pct": float(row['change_pct']),
                    "trend": row['trend'],
                    "model_used": row['model_used']
                })
            
            return history
        
        except Exception as e:
            raise Exception(f"Erro ao buscar histórico: {str(e)}")
    
    def get_processed_data(self, asset: str = "gold") -> pd.DataFrame:
        """
        Retorna dados processados do pipeline
        
        Args:
            asset: Código do ativo
        
        Returns:
            DataFrame com dados processados
        """
        try:
            csv_path = os.path.join(
                self.base_path,
                'processed',
                'gold_features.csv'
            )
            
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")
            
            df = pd.read_csv(csv_path)
            return df
        
        except Exception as e:
            raise Exception(f"Erro ao buscar dados processados: {str(e)}")
