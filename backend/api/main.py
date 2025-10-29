"""
Buongiorno API - FastAPI Backend
API REST para previsão de preços de commodities
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from routers import predictions

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routers import predictions
import uvicorn

# Inicializa aplicação
app = FastAPI(
    title="Buongiorno API",
    description="API de Previsão de Preços de Commodities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS - permite frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternativo
        "https://seu-frontend.vercel.app"  # Deploy futuro
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(predictions.router, prefix="/api", tags=["predictions"])

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