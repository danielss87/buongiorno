"""
Buongiorno - Gold Price Prediction Project
Módulo de engenharia de features
"""

import pandas as pd
import numpy as np

class FeatureEngineer:
    """Classe para criar features a partir dos dados do ouro"""
    
    def __init__(self, df):
        """
        Inicializa o feature engineer
        
        Args:
            df (pd.DataFrame): DataFrame com dados preprocessados
        """
        self.df = df.copy()
        self.feature_df = None
    
    def add_lag_features(self, column='Close', lags=[1, 2, 3, 5, 7]):
        """
        Adiciona features de lag (preços passados)
        
        Args:
            column (str): Coluna para criar lags
            lags (list): Lista de lags a criar
        """
        print(f"⏮️  Adicionando lags de '{column}'...")
        
        for lag in lags:
            self.df[f'{column}_lag_{lag}'] = self.df[column].shift(lag)
        
        print(f"✅ {len(lags)} lags adicionados")
        return self.df
    
    def add_moving_averages(self, column='Close', windows=[7, 14, 30, 60]):
        """
        Adiciona médias móveis
        
        Args:
            column (str): Coluna para calcular médias
            windows (list): Janelas de tempo
        """
        print(f"📊 Adicionando médias móveis de '{column}'...")
        
        for window in windows:
            self.df[f'{column}_MA_{window}'] = self.df[column].rolling(window=window).mean()
        
        print(f"✅ {len(windows)} médias móveis adicionadas")
        return self.df
    
    def add_volatility_features(self, column='Close', windows=[7, 14, 30]):
        """
        Adiciona features de volatilidade
        
        Args:
            column (str): Coluna para calcular volatilidade
            windows (list): Janelas de tempo
        """
        print(f"📈 Adicionando volatilidade de '{column}'...")
        
        for window in windows:
            self.df[f'{column}_volatility_{window}'] = self.df[column].rolling(window=window).std()
        
        print(f"✅ {len(windows)} features de volatilidade adicionadas")
        return self.df
    
    def add_momentum_features(self, column='Close', periods=[5, 10, 20]):
        """
        Adiciona features de momentum (taxa de mudança)
        
        Args:
            column (str): Coluna para calcular momentum
            periods (list): Períodos para momentum
        """
        print(f"🚀 Adicionando momentum de '{column}'...")
        
        for period in periods:
            # Momentum: preço atual - preço N dias atrás
            self.df[f'{column}_momentum_{period}'] = self.df[column] - self.df[column].shift(period)
            
            # Rate of Change (ROC): % de mudança
            self.df[f'{column}_roc_{period}'] = (
                (self.df[column] - self.df[column].shift(period)) / self.df[column].shift(period) * 100
            )
        
        print(f"✅ {len(periods) * 2} features de momentum adicionadas")
        return self.df
    
    def add_price_ranges(self):
        """Adiciona features baseadas em High-Low"""
        print("📏 Adicionando features de range de preço...")
        
        # Range intraday já existe (do fetch_data), mas vamos adicionar variações
        if 'High' in self.df.columns and 'Low' in self.df.columns and 'Close' in self.df.columns:
            # Posição do Close dentro do range
            self.df['close_position'] = (
                (self.df['Close'] - self.df['Low']) / (self.df['High'] - self.df['Low'])
            )
            
            # Range médio móvel
            if 'Intraday_Range' in self.df.columns:
                self.df['avg_range_7'] = self.df['Intraday_Range'].rolling(7).mean()
                self.df['avg_range_30'] = self.df['Intraday_Range'].rolling(30).mean()
        
        print("✅ Features de range adicionadas")
        return self.df
    
    def add_all_features(self, 
                         lags=[1, 2, 3, 5, 7],
                         ma_windows=[7, 14, 30, 60],
                         vol_windows=[7, 14, 30],
                         momentum_periods=[5, 10, 20]):
        """
        Adiciona todas as features de uma vez
        
        Args:
            lags (list): Lags a criar
            ma_windows (list): Janelas para médias móveis
            vol_windows (list): Janelas para volatilidade
            momentum_periods (list): Períodos para momentum
        """
        print("\n🔧 Gerando todas as features...")
        print("=" * 60)
        
        # Adiciona todas as features
        self.add_lag_features(lags=lags)
        self.add_moving_averages(windows=ma_windows)
        self.add_volatility_features(windows=vol_windows)
        self.add_momentum_features(periods=momentum_periods)
        self.add_price_ranges()
        
        # Remove NaNs gerados pelas features
        before = len(self.df)
        self.df = self.df.dropna()
        after = len(self.df)
        
        print("=" * 60)
        print(f"🗑️  Removidas {before - after} linhas com NaN (devido a janelas de features)")
        print(f"✅ Total de features criadas: {len(self.df.columns)}")
        print(f"✅ Registros finais: {after}")
        
        self.feature_df = self.df.copy()
        return self.feature_df
    
    def get_feature_importance_names(self):
        """Retorna lista de nomes de features criadas (útil para modelos)"""
        exclude_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 
                       'Adj Close', 'Median_Price', 'Mean_Price', 
                       'Intraday_Range', 'Intraday_Range_Pct']
        
        feature_cols = [col for col in self.df.columns if col not in exclude_cols]
        return feature_cols
    
    def save_features(self, filepath='data/processed/gold_features.csv'):
        """Salva dados com features"""
        if self.feature_df is None:
            print("⚠️  Execute add_all_features() primeiro")
            return
        
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.feature_df.to_csv(filepath, index=False)
        print(f"💾 Features salvas em: {filepath}")


# Exemplo de uso
if __name__ == "__main__":
    # Carrega dados preprocessados
    df = pd.read_csv('data/processed/gold_processed.csv')
    
    # Cria features
    engineer = FeatureEngineer(df)
    df_features = engineer.add_all_features(
        lags=[1, 2, 3, 5, 7],
        ma_windows=[7, 14, 30],
        vol_windows=[7, 14],
        momentum_periods=[5, 10]
    )
    
    # Salva
    engineer.save_features()
    
    print("\n📊 Amostra dos dados com features:")
    print(df_features[['Date', 'Close', 'Close_lag_1', 'Close_MA_7', 'Close_volatility_7']].head(10))
    
    print("\n📋 Features criadas:")
    feature_names = engineer.get_feature_importance_names()
    for i, feat in enumerate(feature_names, 1):
        print(f"  {i}. {feat}")
