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
        Retorna a última previsão disponível (apenas previsões futuras válidas)

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

            # Converte target_date para datetime
            df['target_date'] = pd.to_datetime(df['target_date'])

            # Filtra apenas previsões futuras (target_date >= hoje)
            today = pd.Timestamp.now().normalize()
            future_predictions = df[df['target_date'] >= today].copy()

            # Se não há previsões futuras, retorna None
            if future_predictions.empty:
                return None

            # Converte prediction_date para datetime e ordena
            future_predictions['prediction_date'] = pd.to_datetime(future_predictions['prediction_date'])
            future_predictions = future_predictions.sort_values('prediction_date', ascending=False)

            # Pega a previsão mais recente (última criada)
            latest = future_predictions.iloc[0]
            
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

    def get_history_with_errors(self, asset: str = "gold") -> List[Dict]:
        """
        Retorna histórico de previsões com erros calculados
        comparando com os valores reais

        Args:
            asset: Código do ativo

        Returns:
            Lista de previsões com erros calculados
        """
        try:
            # Carrega o histórico de previsões
            predictions_path = os.path.join(
                self.base_path,
                'predictions',
                'predictions_history.csv'
            )

            # Carrega os dados reais
            raw_data_path = os.path.join(
                self.base_path,
                'raw',
                'gold_prices.csv'
            )

            if not os.path.exists(predictions_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {predictions_path}")

            if not os.path.exists(raw_data_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {raw_data_path}")

            # Lê os dados
            predictions_df = pd.read_csv(predictions_path)
            raw_df = pd.read_csv(raw_data_path)

            # Converte datas
            predictions_df['target_date'] = pd.to_datetime(predictions_df['target_date'])
            raw_df['Date'] = pd.to_datetime(raw_df['Date'])

            # Monta lista de histórico com erros
            history = []

            for _, pred_row in predictions_df.iterrows():
                target_date = pred_row['target_date']
                predicted_price = float(pred_row['predicted_price'])

                # Busca o preço real na data alvo
                real_data = raw_df[raw_df['Date'] == target_date]

                if not real_data.empty:
                    real_price = float(real_data.iloc[0]['Close'])

                    # Calcula o erro
                    error_abs = predicted_price - real_price
                    error_pct = (error_abs / real_price) * 100

                    history.append({
                        "prediction_date": pred_row['prediction_date'],
                        "target_date": pred_row['target_date'].strftime('%Y-%m-%d'),
                        "predicted_price": predicted_price,
                        "real_price": real_price,
                        "error_abs": round(error_abs, 2),
                        "error_pct": round(error_pct, 2),
                        "model_used": pred_row['model_used'],
                        "model_mape": float(pred_row['model_mape'])
                    })
                else:
                    # Se não tem o valor real ainda, retorna apenas a previsão
                    history.append({
                        "prediction_date": pred_row['prediction_date'],
                        "target_date": pred_row['target_date'].strftime('%Y-%m-%d'),
                        "predicted_price": predicted_price,
                        "real_price": None,
                        "error_abs": None,
                        "error_pct": None,
                        "model_used": pred_row['model_used'],
                        "model_mape": float(pred_row['model_mape'])
                    })

            return history

        except Exception as e:
            raise Exception(f"Erro ao calcular histórico com erros: {str(e)}")
