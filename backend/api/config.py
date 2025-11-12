"""
Buongiorno API - Configuration
Configurações da aplicação e banco de dados
"""

import os
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Database Configuration
# Por padrão usa SQLite para desenvolvimento
# Em produção, pode usar PostgreSQL via variável de ambiente
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{PROJECT_ROOT}/buongiorno.db'
)

# Se estiver usando PostgreSQL no Heroku/Render, converte URL
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# SQLAlchemy Config
SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'

# API Configuration
API_TITLE = "Buongiorno API"
API_VERSION = "2.0.0"
API_DESCRIPTION = "API de Previsão de Preços de Commodities - Arquitetura SaaS"

# Pipeline Configuration
PIPELINE_SECRET = os.getenv("PIPELINE_SECRET", "")

# Asset Configuration
DEFAULT_ASSETS = [
    {
        'code': 'gold',
        'name': 'Ouro',
        'symbol': 'GC=F',
        'description': 'Contratos futuros de ouro (COMEX)',
        'active': True
    },
    {
        'code': 'silver',
        'name': 'Prata',
        'symbol': 'SI=F',
        'description': 'Contratos futuros de prata (COMEX)',
        'active': False
    },
    {
        'code': 'oil',
        'name': 'Petróleo',
        'symbol': 'CL=F',
        'description': 'Petróleo WTI (NYMEX)',
        'active': False
    }
]

# Model Configuration
AVAILABLE_MODELS = ['arima', 'moving_average', 'lstm', 'prophet']
DEFAULT_MODEL = 'arima'
