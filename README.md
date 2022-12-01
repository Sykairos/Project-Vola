# Projet Vola

# Hackathon wild code school 2021 

* Thème : musique
* Durée : 30h  
* Equipe : 5 personnes 


## Définition du projet (suite à un Brainstorming de 3h)

Création d'un système de recommandation de playlists personnalisées, en fonction des goûts utilisateurs, en prenant en compte une ambiance prédite au sein d’un environnement connecté.

## Sourcing

Premier problème rencontré, la récupération des données nécessaires. Après plusieurs heures de recherches sans succès, nous avons été contraints de nous rabattre  sur une base de données déjà en notre possession mais peu fournies, avec l’objectif à terme de l’étoffer de données supplémentaires.

## Elaboration du projet

Après répartition, voilà quelles ont été les différentes tâches du projet:

1. Analyse de la base de données et création de pipelines
    * La base de donnée était déjà clean après vérification exhaustive
2. Renforcement de la base de données en faisant appel à des API (Spotify, via spotipy)
    * Récupération de playlists Spotify
    * Génération de morceaux fictifs, basés sur les moyennes des caractéristiques des morceaux des playlists pour alimenter l’algorithme.
3. Mise en place des algorithmes de machine learning et de navigation dans la database
    * Librairie Scikit-Learn
    * Modèle basé sur le KNN
    * Création de profils type pour chaque genre
4. Création d’une interface graphique, d’une charte graphique, d’un logo et d’une identité d’entreprise 
   * Sourcing d’interface et de charte graphique sur Behance et Adobe Color 
   * Template initial réalisé avec Figma
   * Interface réalisée avec Adobe Illustrator et Tkinter
   * Logo réalisé avec Adobe Illustrator
   * Choix du nom en relation avec l’idée originale de l’entreprise


## Axes d’amélioration

* Créer une interface responsive et la mettre en ligne
* Automatiser l’actualisation de la base de donnée
* Permettre à l’utilisateur d’altérer les playlists en fonction de ses goûts
* Ajuster l’algorithme et les sélections de titre en fonction du comportement de l’utilisateur
* Mener des études sur les différents genres musicaux pour affiner les classifications des morceaux
* Intégrer notre algorithme dans un environnement connecté
* Mettre en place le meilleur moyen de communication et de poursuite du projet.
