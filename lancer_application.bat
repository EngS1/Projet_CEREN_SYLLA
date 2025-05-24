@echo off
python --version >nul 2>&1
if errorlevel 1 (
    echo Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python et l'ajouter au PATH.
    pause
    exit /b
)

set PYTHONPATH=%CD%\src
python -m src.gui
pause