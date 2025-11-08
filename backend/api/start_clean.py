"""
Script para iniciar a API com cache limpo
"""
import os
import sys
import shutil
from pathlib import Path

def clean_pycache():
    """Remove todos os arquivos __pycache__ e .pyc"""
    print("Limpando cache do Python...")

    # Diretório base
    base_dir = Path(__file__).parent

    # Remove __pycache__ directories
    for pycache_dir in base_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            print(f"  [OK] Removido: {pycache_dir.relative_to(base_dir)}")
        except Exception as e:
            print(f"  [!] Erro ao remover {pycache_dir}: {e}")

    # Remove .pyc files
    for pyc_file in base_dir.rglob("*.pyc"):
        try:
            pyc_file.unlink()
            print(f"  [OK] Removido: {pyc_file.relative_to(base_dir)}")
        except Exception as e:
            print(f"  [!] Erro ao remover {pyc_file}: {e}")

    print("Cache limpo!\n")

def start_server():
    """Inicia o servidor uvicorn"""
    print("Iniciando servidor...")
    print("=" * 80)

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_delay=0.5
    )

if __name__ == "__main__":
    clean_pycache()
    start_server()
