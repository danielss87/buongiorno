"""
Buongiorno - Gerador de Previsões Retroativas (Backtest)

Este script gera previsões retroativas usando walk-forward validation:
- Para cada dia no passado (últimos N dias)
- Treina o modelo ARIMA usando apenas dados disponíveis até aquele dia
- Faz a previsão para o próximo dia de trading
- Compara com o valor real
- Salva no predictions_history.csv

Isso permite avaliar a performance real do modelo em condições de produção.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Ignora warnings
warnings.filterwarnings('ignore')


def load_data():
    """Carrega os dados históricos de preços do ouro"""
    data_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'raw',
        'gold_prices.csv'
    )

    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df = df.reset_index(drop=True)

    return df


def train_arima_model(train_data):
    """
    Treina modelo ARIMA nos dados de treino

    Args:
        train_data: Series com preços de fechamento

    Returns:
        Modelo ARIMA treinado
    """
    try:
        # Usa a mesma ordem que o pipeline principal
        order = (5, 1, 0)
        model = ARIMA(train_data, order=order)
        fitted_model = model.fit()
        return fitted_model
    except Exception as e:
        print(f"Erro ao treinar ARIMA: {str(e)}")
        return None


def predict_next_day(model, last_price):
    """
    Faz previsão para o próximo dia

    Args:
        model: Modelo ARIMA treinado
        last_price: Último preço conhecido

    Returns:
        Preço previsto para o próximo dia
    """
    try:
        # Faz previsão para 1 período à frente
        forecast = model.forecast(steps=1)

        # forecast pode ser um array ou series
        if hasattr(forecast, 'iloc'):
            predicted_price = float(forecast.iloc[0])
        else:
            predicted_price = float(forecast[0])

        return predicted_price
    except Exception as e:
        print(f"Erro ao fazer previsao: {str(e)}")
        return None


def calculate_mape(y_true, y_pred):
    """
    Calcula o Mean Absolute Percentage Error (MAPE)

    Args:
        y_true: Valores reais
        y_pred: Valores previstos

    Returns:
        MAPE em porcentagem
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # Remove zeros para evitar divisão por zero
    mask = y_true != 0

    if not mask.any():
        return 0.0

    mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    return mape


def generate_backtest_predictions(num_days=60, min_train_days=252):
    """
    Gera previsões retroativas usando walk-forward validation

    Args:
        num_days: Número de dias no passado para gerar previsões
        min_train_days: Número mínimo de dias de treino (padrão: 252 = 1 ano de trading)

    Returns:
        DataFrame com previsões retroativas
    """
    print("=" * 80)
    print("BUONGIORNO - GERAÇÃO DE PREVISÕES RETROATIVAS (BACKTEST)")
    print("=" * 80)
    print()

    # Carrega dados
    print("[*] Carregando dados historicos...")
    df = load_data()
    print(f"    OK - Dados carregados: {len(df)} dias de historico")
    print(f"    OK - Periodo: {df['Date'].min().strftime('%Y-%m-%d')} ate {df['Date'].max().strftime('%Y-%m-%d')}")
    print()

    # Determina o período de backtest
    last_date = df['Date'].max()
    start_date = last_date - timedelta(days=num_days)

    # Filtra dados após a data de início do backtest
    backtest_df = df[df['Date'] >= start_date].copy()

    print(f"[*] Gerando {num_days} previsoes retroativas...")
    print(f"    Periodo de backtest: {start_date.strftime('%Y-%m-%d')} ate {last_date.strftime('%Y-%m-%d')}")
    print(f"    Minimo de dias de treino: {min_train_days}")
    print()

    predictions = []

    # Para cada dia no período de backtest
    for i in range(len(backtest_df) - 1):  # -1 porque precisamos do próximo dia como target
        current_row = backtest_df.iloc[i]
        next_row = backtest_df.iloc[i + 1]

        current_date = current_row['Date']
        target_date = next_row['Date']
        current_price = current_row['Close']
        real_price = next_row['Close']

        # Pega todos os dados até a data atual para treino
        train_data = df[df['Date'] <= current_date]['Close'].values

        # Verifica se temos dados suficientes para treinar
        if len(train_data) < min_train_days:
            print(f"    [!] Pulando {current_date.strftime('%Y-%m-%d')}: dados insuficientes ({len(train_data)} < {min_train_days})")
            continue

        # Treina o modelo com dados até a data atual
        model = train_arima_model(train_data)

        if model is None:
            print(f"    [X] Erro ao treinar modelo para {current_date.strftime('%Y-%m-%d')}")
            continue

        # Faz previsão para o próximo dia
        predicted_price = predict_next_day(model, current_price)

        if predicted_price is None:
            print(f"    [X] Erro ao fazer previsao para {current_date.strftime('%Y-%m-%d')}")
            continue

        # Calcula métricas
        change_abs = predicted_price - current_price
        change_pct = (change_abs / current_price) * 100

        # Determina tendência
        if change_pct > 0.1:
            trend = "ALTA ↗️"
        elif change_pct < -0.1:
            trend = "BAIXA ↘️"
        else:
            trend = "ESTÁVEL →"

        # Calcula MAPE do modelo (usando últimos 20% dos dados de treino)
        test_size = int(len(train_data) * 0.2)
        test_data = train_data[-test_size:]
        train_subset = train_data[:-test_size]

        # Treina modelo no subset e avalia
        temp_model = train_arima_model(train_subset)
        if temp_model is not None:
            test_predictions = []
            for j in range(len(test_data)):
                pred = temp_model.forecast(steps=1)
                # forecast pode ser um array ou series
                if hasattr(pred, 'iloc'):
                    test_predictions.append(float(pred.iloc[0]))
                else:
                    test_predictions.append(float(pred[0]))
                # Atualiza modelo com novo dado real
                temp_model = temp_model.append([test_data[j]])

            model_mape = calculate_mape(test_data, test_predictions)
        else:
            model_mape = 1.0  # Valor padrão

        # Salva previsão
        predictions.append({
            'prediction_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
            'target_date': target_date.strftime('%Y-%m-%d'),
            'current_price': current_price,
            'predicted_price': predicted_price,
            'change_abs': change_abs,
            'change_pct': change_pct,
            'trend': trend,
            'model_used': 'arima',
            'model_mape': model_mape,
            'real_price': real_price,  # Adicional para análise
            'error_abs': predicted_price - real_price,
            'error_pct': ((predicted_price - real_price) / real_price) * 100
        })

        print(f"    [OK] {current_date.strftime('%Y-%m-%d')} -> {target_date.strftime('%Y-%m-%d')}: "
              f"${current_price:.2f} -> ${predicted_price:.2f} (real: ${real_price:.2f}, "
              f"erro: {((predicted_price - real_price) / real_price) * 100:.2f}%)")

    print()
    print(f"[OK] Geradas {len(predictions)} previsoes retroativas com sucesso!")
    print()

    return pd.DataFrame(predictions)


def save_backtest_predictions(predictions_df, auto_mode=False):
    """
    Salva previsões retroativas no arquivo predictions_history.csv

    Args:
        predictions_df: DataFrame com previsões
        auto_mode: Se True, substitui automaticamente sem perguntar
    """
    csv_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'predictions',
        'predictions_history.csv'
    )

    # Remove colunas extras antes de salvar
    cols_to_keep = ['prediction_date', 'target_date', 'current_price', 'predicted_price',
                   'change_abs', 'change_pct', 'trend', 'model_used', 'model_mape']
    predictions_df = predictions_df[cols_to_keep].copy()

    # Lê histórico existente (se houver)
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
        print(f"[*] Historico existente: {len(existing_df)} registros")

        if auto_mode:
            # Modo automático: substitui tudo
            predictions_df.to_csv(csv_path, index=False)
            print(f"[OK] Historico substituido automaticamente! {len(predictions_df)} previsoes salvas.")
        else:
            # Pergunta se deseja substituir ou adicionar
            print()
            print("Opcoes:")
            print("1. Substituir todo o historico com as novas previsoes retroativas")
            print("2. Adicionar previsoes retroativas ao historico existente (evitando duplicatas)")
            print("3. Cancelar e manter historico atual")
            print()

            choice = input("Escolha uma opcao (1/2/3): ").strip()

            if choice == '1':
                predictions_df.to_csv(csv_path, index=False)
                print(f"[OK] Historico substituido! {len(predictions_df)} previsoes salvas.")

            elif choice == '2':
                # Converte datas para comparação
                existing_df['target_date'] = pd.to_datetime(existing_df['target_date']).dt.strftime('%Y-%m-%d')
                predictions_df['target_date'] = pd.to_datetime(predictions_df['target_date']).dt.strftime('%Y-%m-%d')

                # Remove duplicatas (mantém as novas)
                merged_df = pd.concat([existing_df, predictions_df], ignore_index=True)
                merged_df = merged_df.drop_duplicates(subset=['target_date'], keep='last')
                merged_df = merged_df.sort_values('target_date')

                # Garante que tem apenas as colunas necessárias
                merged_df = merged_df[cols_to_keep]

                merged_df.to_csv(csv_path, index=False)
                print(f"[OK] Historico atualizado! {len(merged_df)} previsoes totais (adicionadas {len(predictions_df)} novas).")

            else:
                print("[X] Operacao cancelada. Historico mantido sem alteracoes.")
                return

    else:
        # Cria novo arquivo
        predictions_df.to_csv(csv_path, index=False)
        print(f"[OK] Novo historico criado! {len(predictions_df)} previsoes salvas.")

    print(f"[*] Arquivo salvo em: {csv_path}")


def main():
    """Função principal"""
    import argparse

    parser = argparse.ArgumentParser(description='Gera previsões retroativas (backtest)')
    parser.add_argument('--days', type=int, default=60, help='Número de dias retroativos (padrão: 60)')
    parser.add_argument('--auto', action='store_true', help='Modo automático: substitui histórico sem perguntar')

    args = parser.parse_args()
    num_days = args.days

    print()
    print(f"Gerando previsões retroativas para os últimos {num_days} dias...")
    print()

    # Gera previsões retroativas
    predictions_df = generate_backtest_predictions(num_days=num_days)

    if predictions_df.empty:
        print("[X] Nenhuma previsao foi gerada.")
        return

    # Mostra estatísticas
    print("=" * 80)
    print("ESTATISTICAS DAS PREVISOES RETROATIVAS")
    print("=" * 80)
    print()

    print(f"Total de previsoes: {len(predictions_df)}")
    print(f"Erro medio absoluto: ${predictions_df['error_abs'].abs().mean():.2f}")
    print(f"Erro medio percentual: {predictions_df['error_pct'].abs().mean():.2f}%")
    print(f"MAPE medio do modelo: {predictions_df['model_mape'].mean():.2f}%")
    print(f"Previsoes com erro < 1%: {len(predictions_df[predictions_df['error_pct'].abs() < 1])} ({(len(predictions_df[predictions_df['error_pct'].abs() < 1]) / len(predictions_df) * 100):.1f}%)")
    print(f"Previsoes com erro < 2%: {len(predictions_df[predictions_df['error_pct'].abs() < 2])} ({(len(predictions_df[predictions_df['error_pct'].abs() < 2]) / len(predictions_df) * 100):.1f}%)")
    print()

    # Salva previsões
    save_backtest_predictions(predictions_df, auto_mode=args.auto)

    print()
    print("=" * 80)
    print("[OK] PROCESSO CONCLUIDO COM SUCESSO!")
    print("=" * 80)


if __name__ == "__main__":
    main()
