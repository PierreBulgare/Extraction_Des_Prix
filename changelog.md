# Change Log

## [Version 0.3.0] - 23/08/2024

### Ajout de fonctionnalités

- **Extraction des données des livres de toutes les catégories** : Le script peut désormais extraire les données de tous les livres de toutes les catégories présentes sur le site.

### Modifications

- **Réorganisation de l'enregistrement des fichiers CSV** : Les fichiers CSV sont désormais enregistrés dans un dossier nommé `Donnees/Par_Livre/(Date de l'extraction)` ou `Donnees/Par_Categorie/(Date de l'extraction)`.
- **Optimisation de l'extraction** : L'extraction des données se fait désormais en multi-threading pour accélérer le temps d'exécution du programme.

## [Version 0.2.1] - 17/08/2024

### Modifications

- **Nommage du fichier de données** : Ajout de la date, de l'heure et du nom du produit ou de la catégorie dans le nom du fichier CSV.

### Corrections

- Correction de bugs mineurs dans la gestion des erreurs inscrites dans le fichier `log.log`.

## [Version 0.2.0] - 17/08/2024

### Ajout de fonctionnalités

- **Extraction de plusieurs livres d'une catégorie** : Le script peut désormais extraire des données pour plusieurs livres appartenant à une même catégorie.
- **Choix du type d'extraction** : L'utilisateur peut choisir entre une extraction individuelle (pour un livre spécifique) ou groupée (pour tous les livres d'une catégorie).

### Modifications

- **Réorganisation et optimisation** : Le code a été réécrit pour améliorer la lisibilité, la modularité et la maintenance du programme.
- **Amélioration de la gestion des erreurs** : Un système de logging a été implémenté pour une meilleure gestion des erreurs lors de l'extraction et de l'enregistrement des données.

### Corrections

- Correction de bugs mineurs.

## [Version 0.1.0] - 16/08/2024

**Première version** : Lancement initial du script avec la fonctionnalité d'extraction des données de base pour un livre spécifique.