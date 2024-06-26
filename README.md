# Challenge Nexialog x MoSEF

## Description

L'objectif de ce challenge était de développer un outil dans l'objectif de modéliser la probabilité de défaut selon 
les normes bâloises. De la préparation des données, à la modélisation en passant par la visualisation des résultats, cet outil a pour but d'accompagner les modélisateurs dans leurs tâches de modélisation. 

## Structure du Projet

Le projet est structuré comme suit :

- `notebooks/` : Dossier contenant les Jupyter Notebooks pour l'analyse et la modélisation.
  - `Analyse_Préparation` : Dossier contenant les Notebooks sur l'analyse exploratoire et la préparation des données. 
  - `Modélisation_Interprétabilité` : Dossier contenant les Notebooks de modélisation, grille de score, segmentation et marge de conservatismes pour notre modèle le plus interprétable
  - `Modélisation_Performance` : Dossier contenant les Notebooks de modélisation, grille de score, segmentation et marge de conservatismes pour notre modèle le plus performant
  - `XGBoost` : Dossier contenant les Notebooks de modélisation, grille de score et segmentation avec un modèle de Boosting.
- `script/` : 
  - `data_preparation` : module python contenant les classes de préparation des données.
  - `Logit_utils` : module python contenant la classe permettant de créer la grille de score du modèle Logit.
  - `XGB_utils` : module python contenant les classes permettant d'entraîner un modèle de xgboost et de créer la grille de score.
- `app/` :
  - `app_utils` : module python contenant les fonctions utiles à l'application
  - `builders` : module python contenant le code html du dashboard
  - `callbacks` : module python contenant les fonctions permettant l'interaction avec le dashboard
  - `plot_analyse` : module python contenant les graphiques pour la partie analyse des données
  - `plot_utils` : module python contenant certains graphiques
  - `vars` : module python contenant les variables

## Pour récupérer le projet

1. Cloner le repository

    ```bash
    git clone https://github.com/Samuel-LP/Challenge_Nexialog.git
    ```

2. Créer un environnement virtuel

   2.1 Pour Windows : 
   
   ```bash
    python -m venv venv
    .\venv\Scripts\activate
   ```
   
   2.2  Pour Mac/Linux : 

   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```

3. Installer les dépendances : 
   ```bash
    pip install -r requirements.txt
   ```

## Pour lancer l'application

Tout d'abord, placez vous à la racine du projet :
```bash
cd Challenge-Nexialog
```

Ensuite, rentrez la commande suivante :

```bash
python app.py
```

Nous n'aurez plus qu'à cliquer sur le lien dans le terminal afin d'utiliser notre application, Nexiamod !
## Authors

- [Jingyi Zhou](https://github.com/ZJY602)
- [Samuel Baheux](https://github.com/SamuelBaheux)
- [Samuel Launay Pariente](https://github.com/samuel-LP)
- [Axel Fritz](https://github.com/AxelFritz1)
