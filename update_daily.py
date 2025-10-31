"""
Buongiorno - Script de Atualização Automática
Roda o pipeline completo e gera nova previsão
"""

import subprocess
import sys
import os
from datetime import datetime
import logging

# Configuração de logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f'update_{datetime.now().strftime("%Y%m%d")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def run_pipeline():
    """Executa o pipeline de previsão"""
    try:
        logger.info("="*70)
        logger.info("🌅 INICIANDO ATUALIZAÇÃO AUTOMÁTICA - BUONGIORNO")
        logger.info("="*70)
        
        # Caminho do script do pipeline
        pipeline_script = os.path.join(
            os.path.dirname(__file__),
            'backend',
            'pipeline',
            'run_pipeline.py'
        )
        
        if not os.path.exists(pipeline_script):
            raise FileNotFoundError(f"Script não encontrado: {pipeline_script}")
        
        logger.info(f"📍 Executando: {pipeline_script}")
        
        # Executa o pipeline
        result = subprocess.run(
            [sys.executable, pipeline_script],
            cwd=os.path.dirname(pipeline_script),
            capture_output=True,
            text=True,
            timeout=600  # Timeout de 10 minutos
        )
        
        # Log da saída
        if result.stdout:
            logger.info("📤 Saída do pipeline:")
            for line in result.stdout.split('\n'):
                if line.strip():
                    logger.info(f"   {line}")
        
        if result.stderr:
            logger.warning("⚠️  Avisos/Erros:")
            for line in result.stderr.split('\n'):
                if line.strip():
                    logger.warning(f"   {line}")
        
        # Verifica se executou com sucesso
        if result.returncode == 0:
            logger.info("✅ Pipeline executado com sucesso!")
            logger.info("="*70)
            return True
        else:
            logger.error(f"❌ Pipeline falhou com código: {result.returncode}")
            logger.error("="*70)
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Timeout: Pipeline demorou mais de 10 minutos")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao executar pipeline: {str(e)}")
        logger.error("="*70)
        return False


def main():
    """Função principal"""
    start_time = datetime.now()
    logger.info(f"⏰ Início: {start_time.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Executa o pipeline
    success = run_pipeline()
    
    # Tempo de execução
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info(f"⏱️  Tempo de execução: {duration:.2f} segundos")
    logger.info(f"🏁 Fim: {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
    
    if success:
        logger.info("🎉 Atualização concluída com sucesso!")
        sys.exit(0)
    else:
        logger.error("💥 Atualização falhou!")
        sys.exit(1)


if __name__ == "__main__":
    main()
