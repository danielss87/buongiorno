@echo off
REM Buongiorno - Script de execução agendada
REM Este arquivo é executado pelo Task Scheduler

echo ============================================
echo Buongiorno - Atualizacao Automatica
echo %date% %time%
echo ============================================

REM Ativa o ambiente conda (AJUSTE O CAMINHO SE NECESSÁRIO)
call C:\Users\danie\miniconda3\Scripts\activate.bat buongiorno-api

REM Navega até a pasta do projeto
cd /d C:\Users\danie\Desktop\Python\buon_giorno

REM Executa o script de atualização
python update_daily.py

REM Pausa se houver erro (para debugging)
if errorlevel 1 (
    echo.
    echo ERRO! Pressione qualquer tecla para sair...
    pause
)