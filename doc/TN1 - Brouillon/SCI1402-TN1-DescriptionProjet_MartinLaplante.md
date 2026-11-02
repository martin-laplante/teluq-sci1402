# Introduction

Ce que l'IA et la science des données a de noble et intéressant à offrir pour la recherche en général, c’est de pouvoir faire émerger ce qu'on ne voit pas immédiatement dans les données, cela permet une catégorisation objective. On pense, entre autres, aux possibilités qu'offre l'apprentissage non supervisé qui permet l'extraction de caractéristiques émergentes d’un corpus de texte. Par exemple, l’analyse d’un groupe de publications d'un site de la NASA, le "Astronomy Picture of the Day" https://apod.nasa.gov/apod/astropix.html.  Ce site opère depuis 1995 et offre à chaque jour une image en lien avec l'astronomie ainsi qu'un texte explicatif. 

Ce projet propose de télécharger le contenu texte de ces articles d'utiliser la compréhension du langage naturel et la factorisation en matrices non négatives pour faire sortir les données cachées.

# Objectifs

## Objectifs principaux
Produire un ensemble de caractéristiques qui soit représentatif de ce que la NASA a accompli en astronomie durant les 30 dernières années.

Concevoir un système suffisament ouvert pour permettre un controle (ex. ajustement d'une fenetre glissante) sur la sortie obtenue.

## Objectifs secondaires
Explorer les visualisations possibles avec les données extraites. La NASA offre un index de ses archives qui suit un modèle chronologique simple et ne montre que les dix dernières années.  Un regroupement comme un index terminologique, sorte de table des matières pourrait s'avérer intéressant.

D'autre part, la programmation orientée objet qu'offre le langage Python est suffisamment avancée pour permettre un développement en composantes réutilisables.  De ce fait, en généralisant suffisamment, d'autre type de corpus pourraient être traité avec ce système, moyennant une réécriture de certaines parties.


# Le pipeline des données

Voici le pipeline de données proposé

## Description des composantes à développer

1. Table d'articles
   - C'est un fichier CSV déposé sur Kaggle, qui contient les explications des photos publiés sur le site APoD.

1. Contrôle fenêtre glissante
   - Bien que le ficher peut être traité en un seul bloc,  l'ajout d'une fenêtre glissante va permettre de localiser dans le temps des caractéristiques plus spécifiques.
   - Une partie de nettoyage devra s'effectuer à ce stade-ci.

1. Compréhension Langage Naturel (NLU)
   - Une fois le bloc de textes sélectionné, on filtre le contenu pour ne garder que les termes significatifs et leur fréquence respective que l'on placera dans une matrice MxN ou M le nombre d'articles et N le nombre de termes significatifs.

1. Factorisation en matrices non négative (NMF)
   - On utilise ici un module spécialisé Python, NumPy qui permet la création de grandes matrices et leurs opérationsé

1. Consolidation
   - Une fois les matrices W et H obtenues, une extraction des caractéristiques va s'effectuer et produire un résultat pour une visualiation

1. Visualisation terminologique
   - Sortie finale un document HTML.

## Méthodologie

Le developpement va suivre un mode Waterfall, car il répond bien au mode de livraison requis le cours, a savoir 

1. Ce document, qui montre les bases du projet, sa motivation, ses objectifs
2. Une version de mi parcours 
3. Une livraison fronctionnelle
4. Rapport final du projet.

Un plan sous forme de charte de Gantt est offert en annexe.

## Chaîne d'outils

### Langage de programmation

Le langage Python est utilisé car il permet:

1. Prototypage rapide; Un minimum de code peut être écrit pour valider ou rejeter une idée en cours de chemin
2. Le langage est à sa 3e version majeure et bénéficie d'une très grande communauté d'utilisateurs, ce qui permet d'obtenir des réponses adéquate à la quasi totalité des problèmes rencontrés pendant le développement
3. Une large comunauté d'utilisateurs signifie également qu'on a accès à un large éventail de librairies, par exemple NumPy dédiée aux opérations numériques complexes (Matrices, Statistiques, etc)

### Documentation électronique

Jupyter est utilisé pour fournir un cahier de note virtuel, fonctionant avec Python.

Grace à Jupyter, un minimum de code de balise peut etre utilisé pour formatter un document facile à lire et pouvant comprendre des exemples de codes Python avec les résultats rééels intégrés.

### Environnement de développement

Durant le certificat, l'utilisation de Google Colab s'est montré extrement utile pour le développement, en particulier pour :
1. Accélération matérielle gratuite, fortement utile pour les scripts ayant un gros volume de données.
2. Les librairies comme Pandas et NumPy sont déjà prêtes à l'emploi
3. Support intégré Jupyter Notebook

## Rôles

### Développement
Tout le code et les livrabres reliés seront produit uniquement par l'étudiant en charge du projet.

### AQ
L'assurance qualité sera effectué par les revisions et évaluation du personnel enseignant TÉLUQ par l'entremise du système de dépot électronique

## Données

### Source
Sur Kaggle un auteur offre une base de presque tous les articles publiés par APOD.  Sous la forme d'un tableau CSV on y trouve la partie "Explanation" de chaque article mis en ligne.  


### Dictionnaire terminologique
Une liste de termes utilisé  est jointe en annexe.

# Références

# Annexes

## A1 - 