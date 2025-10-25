"""
Buongiorno - Gold Price Prediction Project
Pipeline completo de ponta a ponta
"""

import sys
import os

# Adiciona src ao path para imports funcionarem
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import pandas as pd
from src.data.fetch_data import GoldDataFetcher
from src.data.preprocess import DataPreprocessor
from src.features.build_features import FeatureEngineer
from src.models.models import MovingAverageModel, ARIMAModel

class BuongiornoMainPipeline:
    """Pipeline principal do projeto Buongiorno"""
    
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
        self.feature_data = None
        self.models = {}
        self.results = {}
    
    def step1_fetch_data(self, period='5y', force_download=False):
        """
        Passo 1: Buscar dados do Yahoo Finance
        
        Args:
            period (str): Período de dados
            force_download (bool): Força download mesmo se arquivo existir
        """
        print("\n" + "="*70)
        print("🌅 BUONGIORNO - PIPELINE DE PREVISÃO DE PREÇO DO OURO")
        print("="*70)
        print("\n📥 PASSO 1: COLETA DE DADOS")
        print("-"*70)
        
        filepath = 'data/raw/gold_prices.csv'
        
        # Verifica se já existe
        if os.path.exists(filepath) and not force_download:
            print(f"✅ Arquivo já existe: {filepath}")
            print("   Carregando dados existentes...")
            self.raw_data = pd.read_csv(filepath)
            print(f"   {len(self.raw_data)} registros carregados")
        else:
            # Baixa novos dados
            fetcher = GoldDataFetcher()
            self.raw_data = fetcher.fetch_historical_data(period=period)
            self.raw_data = fetcher.calculate_daily_stats()
            fetcher.save_data(filepath)
        
        print(f"✅ Passo 1 concluído: {len(self.raw_data)} registros")
        return self.raw_data
    
    def step2_preprocess(self):
        """Passo 2: Preprocessar dados"""
        print("\n🧹 PASSO 2: PREPROCESSAMENTO")
        print("-"*70)
        
        if self.raw_data is None:
            raise ValueError("Execute step1_fetch_data() primeiro")
        
        preprocessor = DataPreprocessor(self.raw_data)
        self.processed_data = preprocessor.prepare_for_modeling()
        preprocessor.save_processed_data()
        
        print(f"✅ Passo 2 concluído: {len(self.processed_data)} registros")
        return self.processed_data
    
    def step3_feature_engineering(self, 
                                   lags=[1, 2, 3, 5, 7],
                                   ma_windows=[7, 14, 30],
                                   vol_windows=[7, 14],
                                   momentum_periods=[5, 10]):
        """Passo 3: Engenharia de features"""
        print("\n🔧 PASSO 3: ENGENHARIA DE FEATURES")
        print("-"*70)
        
        if self.processed_data is None:
            raise ValueError("Execute step2_preprocess() primeiro")
        
        engineer = FeatureEngineer(self.processed_data)
        self.feature_data = engineer.add_all_features(
            lags=lags,
            ma_windows=ma_windows,
            vol_windows=vol_windows,
            momentum_periods=momentum_periods
        )
        engineer.save_features()
        
        print(f"✅ Passo 3 concluído: {len(self.feature_data)} registros, {len(self.feature_data.columns)} colunas")
        return self.feature_data
    
    def step4_train_models(self):
        """Passo 4: Treinar modelos"""
        print("\n🤖 PASSO 4: TREINAMENTO DE MODELOS")
        print("-"*70)
        
        if self.feature_data is None:
            raise ValueError("Execute step3_feature_engineering() primeiro")
        
        # Divide em treino/teste (80/20)
        split_idx = int(len(self.feature_data) * 0.8)
        train_df = self.feature_data[:split_idx]
        test_df = self.feature_data[split_idx:]
        
        print(f"\n📊 Split de dados:")
        print(f"   Treino: {len(train_df)} registros ({train_df['Date'].min()} a {train_df['Date'].max()})")
        print(f"   Teste:  {len(test_df)} registros ({test_df['Date'].min()} a {test_df['Date'].max()})")
        
        # ==========================================
        # Modelo 1: Média Móvel (Baseline)
        # ==========================================
        print("\n" + "="*70)
        print("🔵 MODELO 1: MÉDIA MÓVEL (7 DIAS)")
        print("="*70)
        
        ma_model = MovingAverageModel(window=7)
        ma_model.fit(self.feature_data)
        ma_metrics = ma_model.evaluate(test_df)
        
        self.models['moving_average'] = ma_model
        self.results['moving_average'] = ma_metrics
        
        # ==========================================
        # Modelo 2: ARIMA
        # ==========================================
        print("\n" + "="*70)
        print("🔵 MODELO 2: ARIMA(5,1,0)")
        print("="*70)
        
        try:
            arima_model = ARIMAModel(order=(5, 1, 0))
            arima_model.fit(train_df['Close'])
            arima_metrics = arima_model.evaluate(test_df['Close'])
            
            self.models['arima'] = arima_model
            self.results['arima'] = arima_metrics
            
        except ImportError:
            print("⚠️  statsmodels não instalado. Pulando ARIMA.")
            print("    Para usar ARIMA, instale: pip install statsmodels")
        
        print(f"\n✅ Passo 4 concluído: {len(self.models)} modelos treinados")
        return self.models
    
    def step5_compare_models(self):
        """Passo 5: Comparar resultados dos modelos"""
        print("\n📊 PASSO 5: COMPARAÇÃO DE MODELOS")
        print("="*70)
        
        if not self.results:
            raise ValueError("Execute step4_train_models() primeiro")
        
        # Cria DataFrame com resultados
        comparison_df = pd.DataFrame(self.results).T
        comparison_df = comparison_df.round(4)
        
        print("\n🏆 Ranking dos Modelos (ordenado por MAPE):")
        print("-"*70)
        comparison_sorted = comparison_df.sort_values('MAPE')
        
        for i, (model_name, row) in enumerate(comparison_sorted.iterrows(), 1):
            print(f"\n{i}. {model_name.upper()}")
            print(f"   MAE:  ${row['MAE']:.2f}")
            print(f"   RMSE: ${row['RMSE']:.2f}")
            print(f"   MAPE: {row['MAPE']:.2f}%")
            print(f"   R²:   {row['R2']:.4f}")
        
        print("\n" + "="*70)
        
        # Salva comparação
        os.makedirs('data/predictions', exist_ok=True)
        comparison_sorted.to_csv('data/predictions/model_comparison.csv')
        print(f"💾 Comparação salva em: data/predictions/model_comparison.csv")
        
        # Guarda o melhor modelo
        self.best_model_name = comparison_sorted.index[0]
        
        return comparison_sorted
    
    def step6_predict_tomorrow(self):
        """Passo 6: Prevê o preço do ouro para amanhã"""
        from datetime import datetime, timedelta
        
        print("\n🔮 PASSO 6: PREVISÃO PARA AMANHÃ")
        print("="*70)
        
        if not self.models:
            raise ValueError("Execute step4_train_models() primeiro")
        
        # Pega o melhor modelo
        best_model = self.models.get(self.best_model_name)
        
        if best_model is None:
            print("⚠️  Modelo não encontrado. Usando ARIMA como padrão.")
            best_model = self.models.get('arima', self.models.get('moving_average'))
        
        print(f"🏆 Usando modelo vencedor: {self.best_model_name.upper()}")
        print("-"*70)
        
        # Pega o último preço conhecido
        last_date = pd.to_datetime(self.feature_data['Date'].iloc[-1])
        last_price = self.feature_data['Close'].iloc[-1]
        
        # Calcula data de amanhã
        tomorrow = last_date + timedelta(days=1)
        
        # Prevê baseado no tipo de modelo
        if self.best_model_name == 'arima':
            # ARIMA: prevê próximo valor
            prediction = best_model.predict_next()
        
        elif self.best_model_name == 'moving_average':
            # Média móvel: usa últimos N dias
            window = best_model.window
            prediction = self.feature_data['Close'].tail(window).mean()
        
        else:
            # Fallback: média móvel simples
            prediction = self.feature_data['Close'].tail(7).mean()
        
        # Calcula variação
        price_change = prediction - last_price
        price_change_pct = (price_change / last_price) * 100
        
        # Determina tendência
        if price_change > 0:
            trend = "ALTA ↗️"
            trend_emoji = "📈"
        elif price_change < 0:
            trend = "BAIXA ↘️"
            trend_emoji = "📉"
        else:
            trend = "ESTÁVEL ➡️"
            trend_emoji = "➡️"
        
        # Mostra resultado na tela
        print(f"\n{trend_emoji} PREVISÃO PARA {tomorrow.strftime('%d/%m/%Y (%A)')}")
        print("-"*70)
        print(f"Preço Atual (hoje):        ${last_price:.2f}")
        print(f"Preço Previsto (amanhã):   ${prediction:.2f}")
        print(f"Variação Esperada:         ${price_change:+.2f} ({price_change_pct:+.2f}%)")
        print(f"Tendência:                 {trend}")
        print("="*70)
        
        # Prepara texto para salvar
        report = f"""
================================================================================
🌅 BUONGIORNO - PREVISÃO DE PREÇO DO OURO
================================================================================

📅 DATA DA PREVISÃO: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
🎯 PREVISÃO PARA:    {tomorrow.strftime('%d/%m/%Y (%A)')}

================================================================================
📊 DADOS ATUAIS
================================================================================
Data Atual:          {last_date.strftime('%d/%m/%Y')}
Preço Atual:         ${last_price:.2f}

================================================================================
🔮 PREVISÃO
================================================================================
Modelo Utilizado:    {self.best_model_name.upper()}
Preço Previsto:      ${prediction:.2f}

Variação Absoluta:   ${price_change:+.2f}
Variação Percentual: {price_change_pct:+.2f}%

Tendência Esperada:  {trend}

================================================================================
📈 INTERPRETAÇÃO
================================================================================
"""
        
        # Adiciona interpretação
        if abs(price_change_pct) < 0.5:
            report += "O mercado deve permanecer ESTÁVEL, com pouca volatilidade esperada.\n"
        elif price_change_pct > 0:
            if price_change_pct > 2:
                report += "FORTE ALTA esperada! Momento favorável para considerar posições compradas.\n"
            else:
                report += "ALTA MODERADA esperada. Tendência positiva no curto prazo.\n"
        else:
            if price_change_pct < -2:
                report += "FORTE BAIXA esperada! Cautela recomendada para posições compradas.\n"
            else:
                report += "BAIXA MODERADA esperada. Tendência negativa no curto prazo.\n"
        
        report += f"""
================================================================================
⚠️  DISCLAIMER
================================================================================
Esta previsão é baseada em modelos estatísticos e dados históricos.
Não constitui recomendação de investimento.
Erro médio do modelo (MAPE): {self.results[self.best_model_name]['MAPE']:.2f}%

================================================================================
Gerado por: Projeto Buongiorno
================================================================================
"""
        
        # Salva em arquivo com data no nome
        filename = f"prediction_{tomorrow.strftime('%Y-%m-%d')}.txt"
        filepath = f"data/predictions/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n💾 Previsão salva em: {filepath}")
        
        # Também salva em CSV para histórico
        csv_data = {
            'prediction_date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'target_date': [tomorrow.strftime('%Y-%m-%d')],
            'current_price': [last_price],
            'predicted_price': [prediction],
            'change_abs': [price_change],
            'change_pct': [price_change_pct],
            'trend': [trend],
            'model_used': [self.best_model_name],
            'model_mape': [self.results[self.best_model_name]['MAPE']]
        }
        
        csv_df = pd.DataFrame(csv_data)
        csv_filename = 'data/predictions/predictions_history.csv'
        
        # Append ao CSV existente ou cria novo
        if os.path.exists(csv_filename):
            csv_df.to_csv(csv_filename, mode='a', header=False, index=False)
        else:
            csv_df.to_csv(csv_filename, index=False)
        
        print(f"💾 Histórico atualizado em: {csv_filename}")
        
        return {
            'date': tomorrow,
            'prediction': prediction,
            'change': price_change,
            'change_pct': price_change_pct,
            'trend': trend
        }
    
    def run_full_pipeline(self):
        """Executa o pipeline completo"""
        try:
            # Passo 1: Coleta de dados
            self.step1_fetch_data(period='5y')
            
            # Passo 2: Preprocessamento
            self.step2_preprocess()
            
            # Passo 3: Feature Engineering
            self.step3_feature_engineering()
            
            # Passo 4: Treinamento de modelos
            self.step4_train_models()
            
            # Passo 5: Comparação de modelos
            self.step5_compare_models()
            
            # Passo 6: Previsão para amanhã
            self.step6_predict_tomorrow()
            
            print("\n" + "="*70)
            print("✅ PIPELINE CONCLUÍDO COM SUCESSO! 🎉")
            print("="*70)
            print("\n💡 Arquivos gerados:")
            print("   📊 Comparação de modelos:  data/predictions/model_comparison.csv")
            print("   🔮 Previsão de amanhã:     data/predictions/prediction_YYYY-MM-DD.txt")
            print("   📈 Histórico de previsões: data/predictions/predictions_history.csv")
            print("   💾 Dados processados:      data/processed/")
            print("   🔧 Features criadas:       data/processed/gold_features.csv")
            print("\n")
            
        except Exception as e:
            print(f"\n❌ Erro no pipeline: {e}")
            import traceback
            traceback.print_exc()


# Execução principal
if __name__ == "__main__":
    print("\n🚀 Iniciando Pipeline Buongiorno...\n")
    
    pipeline = BuongiornoMainPipeline()
    pipeline.run_full_pipeline()
