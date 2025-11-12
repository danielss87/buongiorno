"""
Buongiorno API - FastAPI Backend
API REST para previsão de preços de commodities
ARQUITETURA SAAS - Database-driven
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from routers import predictions, pipeline
from database import init_db
from config import API_TITLE, API_VERSION, API_DESCRIPTION


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Inicializa banco de dados
print("Inicializando banco de dados...")
init_db()
print("Banco de dados pronto!")

# Inicializa aplicação
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS - permite frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server local
        "http://localhost:3000",  # Alternativo local
        "*"  # Permite todos os domínios (ajustar em produção com domínio específico)
    ],
    allow_credentials=False,  # Set to False when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(predictions.router, prefix="/api", tags=["predictions"])
app.include_router(pipeline.router, prefix="/api", tags=["pipeline"])

# Endpoint raiz
@app.get("/")
def root():
    """Endpoint raiz - Health check"""
    return {
        "message": "Buongiorno API v1.0",
        "status": "online",
        "docs": "/docs"
    }

# Endpoint de health check
@app.get("/health")
def health_check():
    """Health check para monitoramento"""
    return {"status": "healthy"}

# Executar servidor (apenas para desenvolvimento local)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload em desenvolvimento
    )