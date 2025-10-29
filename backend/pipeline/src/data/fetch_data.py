"""
Buongiorno - Gold Price Prediction Project
Módulo de coleta de dados do Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

class GoldDataFetcher:
    """Classe para buscar dados históricos do ouro via Yahoo Finance"""
    
    def __init__(self, ticker='GC=F'):
        """
        Inicializa o fetcher
        
        Args:
            ticker (str): Ticker do Yahoo Finance (padrão: GC=F - Gold Futures)
        """
        self.ticker = ticker
        self.data = None
    
    def fetch_historical_data(self, start_date=None, end_date=None, period='max'):
        """
        Busca dados históricos do ouro
        
        Args:
            start_date (str): Data inicial no formato 'YYYY-MM-DD'
            end_date (str): Data final no formato 'YYYY-MM-DD'
            period (str): Período ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max')
        
        Returns:
            pd.DataFrame: DataFrame com dados históricos
        """
        print(f"📊 Buscando dados históricos do ouro ({self.ticker})...")
        
        try:
            if start_date and end_date:
                self.data = yf.download(self.ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
            else:
                self.data = yf.download(self.ticker, period=period, progress=False, auto_adjust=False)
            
            if self.data.empty:
                raise ValueError("Nenhum dado foi retornado")
            
            # Remove colunas multi-level se existirem
            if isinstance(self.data.columns, pd.MultiIndex):
                self.data.columns = self.data.columns.get_level_values(0)
            
            # Adiciona coluna de data como índice explícito
            self.data.reset_index(inplace=True)
            
            print(f"✅ Dados coletados com sucesso!")
            print(f"   Período: {self.data['Date'].min()} a {self.data['Date'].max()}")
            print(f"   Total de registros: {len(self.data)}")
            
            return self.data
            
        except Exception as e:
            print(f"❌ Erro ao buscar dados: {e}")
            return None
    
    def calculate_daily_stats(self):
        """
        Calcula estatísticas diárias (mediana, média, etc)
        Ideal para o conceito 'buongiorno' do projeto
        
        Returns:
            pd.DataFrame: DataFrame com estatísticas diárias
        """
        if self.data is None:
            print("⚠️  Nenhum dado disponível. Execute fetch_historical_data() primeiro.")
            return None
        
        df = self.data.copy()
        
        # Calcula mediana do dia (entre Open, High, Low, Close)
        df['Median_Price'] = df[['Open', 'High', 'Low', 'Close']].median(axis=1)
        
        # Calcula média do dia
        df['Mean_Price'] = df[['Open', 'High', 'Low', 'Close']].mean(axis=1)
        
        # Volatilidade intraday
        df['Intraday_Range'] = df['High'] - df['Low']
        df['Intraday_Range_Pct'] = (df['Intraday_Range'] / df['Open']) * 100
        
        print("✅ Estatísticas diárias calculadas!")
        
        return df
    
    def save_data(self, filepath='data/raw/gold_prices.csv'):
        """
        Salva os dados em CSV
        
        Args:
            filepath (str): Caminho do arquivo CSV
        """
        if self.data is None:
            print("⚠️  Nenhum dado disponível para salvar.")
            return
        
        # Cria diretório se não existir (apenas se houver um diretório no caminho)
        directory = os.path.dirname(filepath)
        if directory:  # Só cria se não for string vazia
            os.makedirs(directory, exist_ok=True)
        
        self.data.to_csv(filepath, index=False)
        print(f"💾 Dados salvos em: {filepath}")
    
    def get_latest_price(self):
        """
        Retorna o preço mais recente
        
        Returns:
            dict: Dicionário com informações do último preço
        """
        if self.data is None or self.data.empty:
            return None
        
        latest = self.data.iloc[-1]
        
        return {
            'date': latest['Date'],
            'open': latest['Open'],
            'high': latest['High'],
            'low': latest['Low'],
            'close': latest['Close'],
            'volume': latest['Volume']
        }
    
    def print_summary(self):
        """Imprime um resumo dos dados coletados"""
        if self.data is None:
            print("⚠️  Nenhum dado disponível.")
            return
        
        latest = self.get_latest_price()
        
        print("\n" + "="*60)
        print("📈 RESUMO DOS DADOS DO OURO")
        print("="*60)
        print(f"Ticker: {self.ticker}")
        print(f"Período: {self.data['Date'].min().strftime('%Y-%m-%d')} a {self.data['Date'].max().strftime('%Y-%m-%d')}")
        print(f"Total de dias: {len(self.data)}")
        print(f"\nÚltimo preço ({latest['date'].strftime('%Y-%m-%d')}):")
        print(f"  Abertura: ${latest['open']:.2f}")
        print(f"  Máxima:   ${latest['high']:.2f}")
        print(f"  Mínima:   ${latest['low']:.2f}")
        print(f"  Fechamento: ${latest['close']:.2f}")
        print("="*60 + "\n")


# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o fetcher
    fetcher = GoldDataFetcher(ticker='GC=F')
    
    # Busca dados históricos (últimos 5 anos para começar)
    data = fetcher.fetch_historical_data(period='5y')
    
    # Calcula estatísticas diárias
    data_with_stats = fetcher.calculate_daily_stats()
    
    # Salva os dados na pasta atual (para teste)
    fetcher.save_data('gold_prices.csv')
    
    # Mostra resumo
    fetcher.print_summary()
    
    # Mostra primeiras linhas
    print("\n📋 Primeiras linhas dos dados:")
    print(data_with_stats.head())
    print("\n📋 Últimas linhas dos dados:")
    print(data_with_stats.tail())