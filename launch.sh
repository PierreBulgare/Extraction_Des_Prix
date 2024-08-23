#!/bin/bash

# Vérifie si pip est installé
if ! command -v pip &> /dev/null
then
    echo "Pip n'est pas présent sur votre ordinateur. Veuillez installer Python avec pip inclus."
    exit 1
fi

# Affiche le message de démarrage de l'installation des librairies
echo "Installation des packages..."

# Installe les packages si nécessaire
pip install --upgrade pip &> /dev/null
pip install -r requirements.txt &> /dev/null

# Lance le fichier main.py
python main.py

# Pause pour permettre de voir l'exécution du script
read -p "Appuyez sur une touche pour continuer..."