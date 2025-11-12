"""
Buongiorno API - Migração CSV → Database
Script para migrar dados existentes dos CSVs para o banco de dados
"""

import sys
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, init_db, reset_db
from repositories.asset_repository import AssetRepository
from repositories.price_repository import PriceRepository
from repositories.prediction_repository import PredictionRepository
from config import DEFAULT_ASSETS


def migrate_assets(db, assets_config):
    """Migra assets para o banco de dados"""
    print("\n📦 MIGRANDO ASSETS...")
    print("=" * 60)

    asset_repo = AssetRepository(db)

    for asset_data in assets_config:
        # Verifica se já existe
        existing = asset_repo.get_by_code(asset_data['code'])

        if existing:
            print(f"   ⏭️  Asset '{asset_data['code']}' já existe, pulando...")
            continue

        # Cria novo asset
        asset = asset_repo.create(
            code=asset_data['code'],
            name=asset_data['name'],
            symbol=asset_data['symbol'],
            description=asset_data['description'],
            active=asset_data['active']
        )
        print(f"   ✅ Asset criado: {asset.code} - {asset.name}")

    print(f"✅ Assets migrados com sucesso!")


def migrate_prices(db, pipeline_data_path):
    """Migra preços históricos dos CSVs para o banco de dados"""
    print("\n📈 MIGRANDO PREÇOS HISTÓRICOS...")
    print("=" * 60)

    asset_repo = AssetRepository(db)
    price_repo = PriceRepository(db)

    # Por enquanto apenas gold
    csv_path = pipeline_data_path / 'raw' / 'gold_prices.csv'

    if not csv_path.exists():
        print(f"   ⚠️  Arquivo não encontrado: {csv_path}")
        return

    # Carrega CSV
    df = pd.read_csv(csv_path)
    print(f"   📊 {len(df)} registros encontrados no CSV")

    # Busca o asset gold
    asset = asset_repo.get_by_code('gold')
    if not asset:
        print("   ❌ Asset 'gold' não encontrado! Execute migrate_assets primeiro")
        return

    # Migra em lotes para melhor performance
    batch_size = 500
    total_migrated = 0

    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        prices_to_insert = []

        for _, row in batch.iterrows():
            # Converte data
            price_date = pd.to_datetime(row['Date']).date()

            # Verifica se já existe
            existing = price_repo.get_by_asset_and_date(asset.id, price_date)
            if existing:
                continue

            prices_to_insert.append({
                'asset_id': asset.id,
                'date': price_date,
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'adj_close': float(row.get('Adj Close', row['Close'])),
                'volume': float(row.get('Volume', 0))
            })

        if prices_to_insert:
            price_repo.bulk_create(prices_to_insert)
            total_migrated += len(prices_to_insert)
            print(f"   💾 Lote {i//batch_size + 1}: {len(prices_to_insert)} preços inseridos")

    print(f"✅ Total de preços migrados: {total_migrated}")


def migrate_predictions(db, pipeline_data_path):
    """Migra previsões históricas dos CSVs para o banco de dados"""
    print("\n🔮 MIGRANDO PREVISÕES HISTÓRICAS...")
    print("=" * 60)

    asset_repo = AssetRepository(db)
    prediction_repo = PredictionRepository(db)

    # Por enquanto apenas gold
    csv_path = pipeline_data_path / 'predictions' / 'predictions_history.csv'

    if not csv_path.exists():
        print(f"   ⚠️  Arquivo não encontrado: {csv_path}")
        return

    # Carrega CSV
    df = pd.read_csv(csv_path)
    print(f"   📊 {len(df)} registros encontrados no CSV")

    # Busca o asset gold
    asset = asset_repo.get_by_code('gold')
    if not asset:
        print("   ❌ Asset 'gold' não encontrado! Execute migrate_assets primeiro")
        return

    # Migra cada previsão
    total_migrated = 0

    for _, row in df.iterrows():
        try:
            # Parse dates
            prediction_date = pd.to_datetime(row['prediction_date'])
            target_date = pd.to_datetime(row['target_date']).date()

            # Parse trend
            trend_text = str(row['trend']).lower()
            if 'alta' in trend_text or '↗' in trend_text:
                trend = 'up'
            elif 'baixa' in trend_text or '↘' in trend_text:
                trend = 'down'
            else:
                trend = 'stable'

            # Calcula confidence
            model_mape = float(row['model_mape'])
            if model_mape < 1:
                confidence = 'high'
            elif model_mape < 2:
                confidence = 'medium'
            else:
                confidence = 'low'

            # Cria previsão
            prediction_repo.create(
                asset_id=asset.id,
                prediction_date=prediction_date,
                target_date=target_date,
                current_price=float(row['current_price']),
                predicted_price=float(row['predicted_price']),
                change_abs=float(row['change_abs']),
                change_pct=float(row['change_pct']),
                trend=trend,
                model_used=row['model_used'],
                model_mape=model_mape,
                confidence=confidence
            )

            total_migrated += 1

            if total_migrated % 50 == 0:
                print(f"   💾 {total_migrated} previsões migradas...")

        except Exception as e:
            print(f"   ⚠️  Erro ao migrar linha: {e}")
            continue

    print(f"✅ Total de previsões migradas: {total_migrated}")


def main():
    """Executa a migração completa"""
    print("\n" + "=" * 60)
    print("BUONGIORNO - MIGRACAO CSV -> DATABASE")
    print("=" * 60)

    # Caminho para os dados do pipeline
    project_root = Path(__file__).parent.parent.parent
    pipeline_data_path = project_root / 'backend' / 'pipeline' / 'data'

    print(f"\n📂 Diretório de dados: {pipeline_data_path}")

    # Confirma reset do banco
    print("\n⚠️  ATENÇÃO: Esta operação irá RESETAR o banco de dados!")
    print("   Todos os dados existentes serão APAGADOS.")
    response = input("\nDeseja continuar? (sim/não): ")

    if response.lower() not in ['sim', 's', 'yes', 'y']:
        print("\n❌ Migração cancelada pelo usuário")
        return

    # Reseta banco de dados
    print("\n🔄 Resetando banco de dados...")
    reset_db()

    # Cria sessão do banco
    db = SessionLocal()

    try:
        # Migra assets
        migrate_assets(db, DEFAULT_ASSETS)

        # Migra prices
        migrate_prices(db, pipeline_data_path)

        # Migra predictions
        migrate_predictions(db, pipeline_data_path)

        print("\n" + "=" * 60)
        print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO! 🎉")
        print("=" * 60)

        # Mostra estatísticas
        from repositories.asset_repository import AssetRepository
        from repositories.price_repository import PriceRepository
        from repositories.prediction_repository import PredictionRepository

        asset_repo = AssetRepository(db)
        price_repo = PriceRepository(db)
        prediction_repo = PredictionRepository(db)

        print("\n📊 ESTATÍSTICAS:")
        print(f"   Assets: {len(asset_repo.get_all())}")
        print(f"   Preços: {price_repo.count_by_asset(1)}")  # gold = 1
        print(f"   Previsões: {prediction_repo.count_by_asset(1)}")

    except Exception as e:
        print(f"\n❌ Erro durante migração: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
