# Game Database Analyzer

Ce projet est une application web créée avec Dash qui permet d'analyser une base de données de ventes de jeux vidéo.

## Installation

1. Clonez ce dépôt sur votre machine locale.
2. Assurez-vous d'avoir Python installé sur votre système.
3. Installez les dépendances requises en exécutant les commandes suivantes :

```python
pip install dash
pip install pandas
pip install plotly
```

## Utilisation

1. Assurez-vous d'avoir une base de données de ventes de jeux vidéo au format CSV nommée `vgsales.csv` dans le même répertoire que le code.
2. Lancez l'application en exécutant le fichier `app.py` :

````python
python app.py
````

3. Accédez à l'application dans votre navigateur en ouvrant l'URL indiquée dans la console.

## Fonctionnalités

- Recherche de jeux par nom.
- Filtrage des jeux par année, éditeur, genre et plateforme.
- Affichage des jeux filtrés dans un tableau interactif.
- Visualisation des ventes par région sous forme de graphique circulaire, mis à jour en temps réel en fonction des filtres sélectionnés.

## Auteur

Ce projet a été réalisé par Lukas CHAMI, Enzo Nussbaum et Benedict Nenere.
