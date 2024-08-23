@echo off
REM Vérifie si pip est installé
python -m pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Pip n'est pas présent sur votre ordinateur. Veuillez installer Python avec pip inclus.
    pause
    exit /b
)

REM Affiche le message de démarrage de l'installation des librairies
echo Installation des packages...

REM Installe les packages si nécessaire
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt >nul 2>&1

REM Lance le fichier main.py
python main.py

pause