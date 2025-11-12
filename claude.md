## Objetivo do projeto
Testar diferentes modelos e metodologias de previsão em ciência de dados para diferentes ativos financeiros (ouro, ações, commodities, etc).

## Da visão estratégica/de negócio do projeto
A provocação de negócio que o projeto se faz é: em um mundo onde bancos e fundos de investimento possuem super computadores, como o pequeno investidor poderia se beneficiar de modelos estatísticos, redes neurais e ciência de dados? O buongiorno é uma proposta de produto que poderia ser utilizado pelo investidor de varejo. Esta ferramenta se propõe a ter os dados necessários para uma tomada de decisão de uma vez por dia, buscando prever o preço dos ativos no dia seguinte, bem como a sua tendência (aumento de preço, diminuição de preço).

## A Arquitetura do projeto

### Visão Geral
A arquitetura é de uma aplicação web moderna, com back-end feito em Python e FastAPI, e o front-end feito com React e Vite. O padrão de design system tem forte inspiração no Untitled UI.

A arquitetura é modular e 'à prova de futuro', seguindo as melhores práticas de produtos SaaS modernos, distanciando-se completamente de sua origem como projeto com arquitetura de 'notebook'.

### Arquitetura do Backend (Database-Driven)

A aplicação agora utiliza **banco de dados relacional** (SQLite em desenvolvimento, preparado para PostgreSQL em produção) ao invés de arquivos CSV. Esta mudança fundamental traz:

#### Camadas da Arquitetura

```
backend/api/
├── models/                 # ORM Models (SQLAlchemy)
│   ├── asset.py           # Ativos financeiros
│   ├── price.py           # Preços históricos
│   ├── prediction.py      # Previsões geradas
│   └── model_run.py       # Metadados de execuções
│
├── repositories/          # Data Access Layer
│   ├── asset_repository.py
│   ├── price_repository.py
│   └── prediction_repository.py
│
├── services/             # Business Logic Layer
│   └── prediction_service.py
│
├── routers/              # API Endpoints
│   ├── predictions.py
│   └── pipeline.py
│
├── database.py           # DB Connection & Session
├── config.py             # Configurações
└── main.py              # FastAPI Application
```

#### Benefícios da Arquitetura Database-Driven:

1. **Escalabilidade**: Preparado para múltiplos usuários e ativos
2. **Integridade**: Constraints e foreign keys garantem consistência
3. **Performance**: Queries otimizadas com índices
4. **Flexibilidade**: Fácil adicionar novos ativos e modelos
5. **Padrão Repository**: Separação clara entre data access e business logic
6. **Dependency Injection**: FastAPI Depends para gestão de sessões
7. **Migrations**: Schema versionado (futuro Alembic)
8. **Multi-tenant Ready**: Preparado para expansão futura

### Frontend (React + Vite)

O frontend permanece como SPA moderna com:
- React 19 para componentes
- Vite para build otimizado
- Tailwind CSS inspirado no Untitled UI
- Comunicação via API REST

### Pipeline de Dados

O pipeline agora salva dados diretamente no banco:
1. Coleta de dados (Yahoo Finance)
2. Preprocessamento e feature engineering
3. Treinamento de modelos
4. **Salva previsões no database** (não mais em CSV)
5. API consome do database via repositories

### Migração de Dados

Script `migrate_csv_to_db.py` para migrar dados históricos dos CSVs para o database. Executar uma única vez na transição. 

