import sys
import os
import math
import requests
import logging
from bs4 import BeautifulSoup

# Log File
LOG_FILE = "log.log"

# Message d'erreur générique
def display_default_error_message():
    print("Une erreur a été détecté. Consultez le fichier log.log pour plus de détails.")

def setup_logging():
    """Système de logging pour la maintenance de l'application et la gestion d'éventuelle erreurs."""
    # Configuration du module de logging
    logging.basicConfig(
        filename=LOG_FILE, # Fichier où seront enregistrés les logs
        level=logging.INFO,  # Niveaux de log qui pourront être enregistrés : INFO, WARNING, ERROR, CRITICAL
        format="%(asctime)s - %(levelname)s - %(message)s", # Format des messages de log
        datefmt="%d-%m-%Y %H:%M:%S", # Format de la date et l'heure dans le fichier
        encoding='utf-8' # Encodage pour afficher les caractères spéciaux et accents dans les logs
    )

def create_log():
    """Vérifie et crée un fichier log s'il n'existe pas."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding="utf-8") as log_file:
            pass  # Création d'un fichier log vide

setup_logging()
create_log()