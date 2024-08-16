@echo off
REM Vérifier si pip est installé
python -m pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Pip n'est pas présent sur votre ordinateur. Veuillez installer Python avec pip inclus.
    pause
    exit /b
)

REM Afficher le message de démarrage de l'installation des librairies
echo Installation des packages...

REM Installation des packages si nécessaire
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt >nul 2>&1

REM Lancer le fichier main.py
python main.py

pause