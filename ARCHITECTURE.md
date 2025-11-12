# Arquitetura Buongiorno - Database-Driven

## Visão Geral

O projeto foi refatorado de uma arquitetura baseada em CSV para uma arquitetura SaaS moderna utilizando banco de dados relacional.

## Stack Tecnológica

- **Backend**: FastAPI + SQLAlchemy
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: React 19 + Vite
- **Styling**: Tailwind CSS

## Estrutura do Backend

### Models (ORM)
```
backend/api/models/
├── asset.py        # Ativos financeiros (gold, silver, oil)
├── price.py        # Preços históricos diários
├── prediction.py   # Previsões geradas pelos modelos
└── model_run.py    # Metadata de execuções do pipeline
```

### Repositories (Data Access Layer)
```
backend/api/repositories/
├── asset_repository.py      # CRUD de assets
├── price_repository.py      # Gestão de preços (bulk insert, queries)
└── prediction_repository.py # Previsões (com cálculo de erros)
```

### Services (Business Logic)
```
backend/api/services/
└── prediction_service.py    # Lógica de negócio para previsões
```

### API Routers
```
backend/api/routers/
├── predictions.py  # Endpoints de previsões
└── pipeline.py     # Trigger do pipeline
```

## Padrões Implementados

### 1. Repository Pattern
Separa data access da business logic:
```python
# Repository faz queries
class PredictionRepository:
    def get_latest_by_asset(self, asset_id):
        return self.db.query(Prediction)...

# Service usa repository
class PredictionService:
    def __init__(self, db):
        self.prediction_repo = PredictionRepository(db)
```

### 2. Dependency Injection
FastAPI Depends gerencia sessões do banco:
```python
@router.get("/predictions/latest")
def get_latest(db: Session = Depends(get_db)):
    service = PredictionService(db)
    return service.get_latest_prediction()
```

### 3. ORM Models
SQLAlchemy define schema e relationships:
```python
class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    asset = relationship("Asset", back_populates="predictions")
```

## Setup Inicial

### 1. Criar Database
```bash
cd backend/api
python -c "from database import init_db; init_db()"
```

### 2. Migrar Dados CSV (uma vez)
```python
python -c "
from database import SessionLocal, reset_db
from repositories import AssetRepository, PriceRepository, PredictionRepository
# ... ver migrate_csv_to_db.py para script completo
"
```

### 3. Rodar API
```bash
cd backend/api
python main.py
```

## Endpoints Principais

- `GET /api/predictions/latest` - Última previsão
- `GET /api/predictions/history` - Histórico de previsões
- `GET /api/predictions/history-errors` - Histórico com erros calculados
- `GET /api/assets` - Lista de ativos
- `POST /api/pipeline/run` - Trigger do pipeline

## Database Schema

### Assets
- id, code, name, symbol, description, active

### Prices
- id, asset_id, date, open, high, low, close, adj_close, volume

### Predictions
- id, asset_id, prediction_date, target_date
- current_price, predicted_price, real_price
- change_abs, change_pct, trend
- model_used, model_mape, confidence
- error_abs, error_pct (calculado quando real_price existe)

### Model Runs
- id, run_date, status, model_name
- mae, rmse, mape, r2_score
- train_size, test_size, duration_seconds

## Próximos Passos

1. **Pipeline Integration**: Atualizar pipeline para salvar no DB
2. **Alembic Migrations**: Versionamento do schema
3. **PostgreSQL em Produção**: Trocar SQLite por PostgreSQL
4. **Autenticação**: Adicionar JWT auth
5. **Multi-tenancy**: Suporte a múltiplos usuários
6. **Caching**: Redis para cache de queries
7. **Background Jobs**: Celery para execução assíncrona do pipeline
