# Game Database Analyzer et devine le jeu

Ce projet ontient deux applications Web construites avec Dash, une bibliothèque Python pour créer des applications web analytiques interactives.

## prérequis

1. Clonez ce dépôt sur votre machine locale.
2. Assurez-vous d'avoir Python installé sur votre système.
3. Installez les dépendances requises en exécutant les commandes suivantes :

```python
pip install dash
pip install pandas
pip install plotly
```

## Le jeu vidéo (main.py)

### aperçu du jeu

Dans cette application, les utilisateurs sont invités à deviner le nom d'un jeu vidéo en fonction des indices donnés. Le jeu tire aléatoirement un jeu vidéo à partir d'un ensemble de données de ventes de jeux vidéo et fournit des indices concernant ce jeu. Vous avez 5 chances pour trouver le jeu.

A noter que le jeu est en version Beta, plusieurs bugs peuvent apparaître pouvant gêner la bonne utilisation du jeu, désolé par avance.

### exécution du jeu

Pour exécuter cette application, assurez-vous d'avoir Python et les bibliothèques requises installés. Exécutez ensuite le fichier main.py et accédez à l'application via votre navigateur web.

```python
python main.py
```

## Game Database Analyzer (app.py)

### aperçu de l'analyse

Cette application fournit une interface interactive pour explorer une base de données de ventes de jeux vidéo. Les utilisateurs peuvent filtrer les jeux par année, éditeur, genre et plateforme, et visualiser les données filtrées sous forme de tableau et de graphiques.

### exécution de l'analyse

Pareil pour exécuter cette application, assurez-vous d'avoir Python et les bibliothèques requises installés. Exécutez ensuite le fichier app.py et accédez à l'application via votre navigateur web.

```python
python app.py
```

## Auteurs

Ce projet a été réalisé par Lukas Chami, Enzo Nussbaum et Benedict Nenert.
