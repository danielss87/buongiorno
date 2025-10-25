"""
Buongiorno - Gold Price Prediction Project
Módulo de modelos de previsão
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class BaseModel:
    """Classe base para todos os modelos"""
    
    def __init__(self, name="Base Model"):
        self.name = name
        self.model = None
        self.predictions = None
        self.metrics = {}
    
    def calculate_metrics(self, y_true, y_pred):
        """Calcula métricas de avaliação"""
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        r2 = r2_score(y_true, y_pred)
        
        self.metrics = {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'R2': r2
        }
        
        return self.metrics
    
    def print_metrics(self):
        """Imprime métricas formatadas"""
        print(f"\n📊 Métricas do modelo: {self.name}")
        print("=" * 50)
        print(f"MAE (Mean Absolute Error):     ${self.metrics['MAE']:.2f}")
        print(f"RMSE (Root Mean Squared Error): ${self.metrics['RMSE']:.2f}")
        print(f"MAPE (Mean Absolute % Error):   {self.metrics['MAPE']:.2f}%")
        print(f"R² Score:                       {self.metrics['R2']:.4f}")
        print("=" * 50)


class MovingAverageModel(BaseModel):
    """Modelo baseline: Média Móvel Simples"""
    
    def __init__(self, window=7):
        super().__init__(name=f"Moving Average ({window} days)")
        self.window = window
    
    def fit(self, df, target_col='Close'):
        """Calcula a média móvel (não precisa treinar)"""
        self.target_col = target_col
        return self
    
    def predict(self, df):
        """Prevê usando média móvel"""
        # A previsão de amanhã é a média dos últimos N dias
        predictions = df[self.target_col].rolling(window=self.window).mean()
        
        # Shift para prever o próximo dia
        self.predictions = predictions.shift(1)
        
        return self.predictions
    
    def evaluate(self, df):
        """Avalia o modelo"""
        if self.predictions is None:
            self.predict(df)
        
        # Remove NaNs
        mask = ~(self.predictions.isna() | df[self.target_col].isna())
        y_true = df[self.target_col][mask]
        y_pred = self.predictions[mask]
        
        self.calculate_metrics(y_true, y_pred)
        self.print_metrics()
        
        return self.metrics


class ARIMAModel(BaseModel):
    """Modelo ARIMA para séries temporais"""
    
    def __init__(self, order=(5, 1, 0)):
        super().__init__(name=f"ARIMA{order}")
        self.order = order
        self.history = []
    
    def fit(self, train_series):
        """
        Treina o modelo ARIMA
        
        Args:
            train_series (pd.Series): Série temporal de treino
        """
        try:
            from statsmodels.tsa.arima.model import ARIMA
        except ImportError:
            print("❌ statsmodels não instalado. Execute: pip install statsmodels")
            return None
        
        print(f"🔧 Treinando {self.name}...")
        
        self.history = list(train_series)
        
        # Treina modelo inicial
        model = ARIMA(self.history, order=self.order)
        self.model = model.fit()
        
        print(f"✅ {self.name} treinado!")
        return self
    
    def predict_next(self):
        """Prevê o próximo valor"""
        from statsmodels.tsa.arima.model import ARIMA
        
        # Retreina com histórico atualizado
        model = ARIMA(self.history, order=self.order)
        model_fit = model.fit()
        
        # Prevê próximo passo
        forecast = model_fit.forecast(steps=1)
        
        return forecast[0]
    
    def walk_forward_validation(self, test_series):
        """
        Validação walk-forward (mais realista para séries temporais)
        Prevê um dia por vez, adicionando o valor real ao histórico
        """
        print(f"🚶 Executando walk-forward validation com {len(test_series)} passos...")
        
        predictions = []
        
        for i, true_value in enumerate(test_series):
            # Prevê próximo valor
            pred = self.predict_next()
            predictions.append(pred)
            
            # Adiciona valor real ao histórico
            self.history.append(true_value)
            
            if (i + 1) % 50 == 0:
                print(f"   Progresso: {i + 1}/{len(test_series)} previsões")
        
        self.predictions = np.array(predictions)
        
        print("✅ Walk-forward validation concluída!")
        return self.predictions
    
    def evaluate(self, test_series):
        """Avalia o modelo no conjunto de teste"""
        if self.predictions is None:
            self.walk_forward_validation(test_series)
        
        y_true = test_series.values
        y_pred = self.predictions
        
        self.calculate_metrics(y_true, y_pred)
        self.print_metrics()
        
        return self.metrics


class HybridModel(BaseModel):
    """Modelo híbrido: combina diferentes abordagens"""
    
    def __init__(self, models, weights=None):
        super().__init__(name="Hybrid Model")
        self.models = models
        
        # Pesos iguais se não especificado
        if weights is None:
            self.weights = [1/len(models)] * len(models)
        else:
            self.weights = weights
    
    def fit(self, *args, **kwargs):
        """Treina todos os modelos"""
        print(f"🔧 Treinando {len(self.models)} modelos do ensemble...")
        
        for model in self.models:
            model.fit(*args, **kwargs)
        
        print("✅ Todos os modelos treinados!")
        return self
    
    def predict(self, *args, **kwargs):
        """Combina previsões de todos os modelos"""
        all_predictions = []
        
        for model in self.models:
            pred = model.predict(*args, **kwargs)
            all_predictions.append(pred)
        
        # Média ponderada
        self.predictions = np.average(all_predictions, axis=0, weights=self.weights)
        
        return self.predictions


# Exemplo de uso
if __name__ == "__main__":
    # Carrega dados com features
    df = pd.read_csv('data/processed/gold_features.csv')
    
    # Divide em treino/teste (80/20)
    split_idx = int(len(df) * 0.8)
    train_df = df[:split_idx]
    test_df = df[split_idx:]
    
    print(f"📊 Dataset:")
    print(f"   Treino: {len(train_df)} registros")
    print(f"   Teste:  {len(test_df)} registros")
    
    # ==========================================
    # Modelo 1: Média Móvel (Baseline)
    # ==========================================
    print("\n" + "="*60)
    print("🔵 MODELO 1: MÉDIA MÓVEL (BASELINE)")
    print("="*60)
    
    ma_model = MovingAverageModel(window=7)
    ma_model.fit(df)
    ma_model.evaluate(test_df)
    
    # ==========================================
    # Modelo 2: ARIMA
    # ==========================================
    print("\n" + "="*60)
    print("🔵 MODELO 2: ARIMA")
    print("="*60)
    
    try:
        arima_model = ARIMAModel(order=(5, 1, 0))
        arima_model.fit(train_df['Close'])
        arima_model.evaluate(test_df['Close'])
    except ImportError:
        print("⚠️  Instale statsmodels: pip install statsmodels")
    
    print("\n✅ Avaliação de modelos concluída!")
