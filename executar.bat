@echo off
echo Iniciando Sistema de Validacao de Guias...
echo.

REM Verifica se o Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Execute primeiro: instalar_dependencias.bat
    pause
    exit /b 1
)

REM Verifica se o arquivo principal existe
if not exist "validacao_guias.py" (
    echo ERRO: Arquivo validacao_guias.py nao encontrado!
    pause
    exit /b 1
)

echo Executando aplicacao...
python validacao_guias.py

if errorlevel 1 (
    echo.
    echo A aplicacao foi encerrada com erro.
    pause
)

echo.
echo Aplicacao encerrada.
pause

