"""
Buongiorno - Gold Price Prediction Project
Módulo de preprocessamento de dados
"""

import pandas as pd
import numpy as np
from datetime import datetime

class DataPreprocessor:
    """Classe para preprocessar e limpar dados do ouro"""
    
    def __init__(self, df):
        """
        Inicializa o preprocessor
        
        Args:
            df (pd.DataFrame): DataFrame com dados brutos
        """
        self.df = df.copy()
        self.processed_df = None
    
    def clean_data(self):
        """Remove dados faltantes e inconsistentes"""
        print("🧹 Limpando dados...")
        
        # Remove linhas com valores nulos
        before = len(self.df)
        self.df = self.df.dropna()
        after = len(self.df)
        
        if before > after:
            print(f"   Removidas {before - after} linhas com valores nulos")
        
        # Garante que Date é datetime
        if 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Ordena por data
        self.df = self.df.sort_values('Date').reset_index(drop=True)
        
        print(f"✅ Dados limpos: {len(self.df)} registros")
        return self.df
    
    def add_temporal_features(self):
        """Adiciona features temporais (dia da semana, mês, etc)"""
        print("📅 Adicionando features temporais...")
        
        if 'Date' not in self.df.columns:
            print("⚠️  Coluna 'Date' não encontrada")
            return self.df
        
        self.df['day_of_week'] = self.df['Date'].dt.dayofweek
        self.df['month'] = self.df['Date'].dt.month
        self.df['quarter'] = self.df['Date'].dt.quarter
        self.df['day_of_month'] = self.df['Date'].dt.day
        self.df['week_of_year'] = self.df['Date'].dt.isocalendar().week
        
        print("✅ Features temporais adicionadas")
        return self.df
    
    def prepare_for_modeling(self):
        """Prepara dados finais para modelagem"""
        print("\n🔧 Preparando dados para modelagem...")
        
        # Limpa dados
        self.clean_data()
        
        # Adiciona features temporais
        self.add_temporal_features()
        
        self.processed_df = self.df.copy()
        
        print("✅ Dados preparados!")
        print(f"   Shape: {self.processed_df.shape}")
        print(f"   Colunas: {list(self.processed_df.columns)}")
        
        return self.processed_df
    
    def save_processed_data(self, filepath='data/processed/gold_processed.csv'):
        """Salva dados processados"""
        if self.processed_df is None:
            print("⚠️  Execute prepare_for_modeling() primeiro")
            return
        
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.processed_df.to_csv(filepath, index=False)
        print(f"💾 Dados processados salvos em: {filepath}")


# Exemplo de uso
if __name__ == "__main__":
    # Carrega dados brutos
    df = pd.read_csv('data/raw/gold_prices.csv')
    
    # Preprocessa
    preprocessor = DataPreprocessor(df)
    df_processed = preprocessor.prepare_for_modeling()
    
    # Salva
    preprocessor.save_processed_data()
    
    print("\n📊 Primeiras linhas dos dados processados:")
    print(df_processed.head())
