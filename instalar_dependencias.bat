@echo off
echo Instalando dependencias do Sistema de Validacao de Guias...
echo.

REM Verifica se o Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale o Python 3.8 ou superior antes de continuar.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado!
python --version

echo.
echo Instalando bibliotecas necessarias...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERRO: Falha na instalacao das dependencias!
    echo Verifique sua conexao com a internet e tente novamente.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para executar o sistema:
echo python validacao_guias.py
echo.
echo Antes de usar, configure:
echo 1. Copie config_exemplo.py para config.py
echo 2. Ajuste as configuracoes do banco de dados
echo 3. Teste a conexao
echo.
pause

