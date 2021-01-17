# Projet-PythonDataViz-E3FI

 Ce projet permet de générer un dashboard interactif sur les émissions de CO2 dans le monde
 depuis des fichiers au format .csv récupérer dynamiquement sur https://databank.worldbank.org/.  

 Le dashboard contient plusieurs graphiques sur les émissions totales de CO2 dans
 le monde, les émissions par habitants et également par rapport aux émissions
 en fonction du pouvoir d'achat relatif au PIB des différents pays.  
 
 Parmi ces graphiques, on y retrouve: 
 - Une carte du monde avec des données géolocalisées
 - Un diagramme circulaire
 - Un histogramme
 - Un diagramme à barre 
 - Un diagramme à point pour chaque pays
 
 
## User Guide:

1. Télécharger le projet depuis Github
2. Extraire le dossier
3. Naviguer dans le dossier depuis l'invite de commande Windows our le terminal Linux
4. Utiliser le gestionnaire de paquets [pip](https://pip.pypa.io/en/stable/) pour installer les modules nécessaires.  
   Les modules nécessaires sont `pandas`, `plotly`, `plotly_express`, `dash`,
`dash_bootstrap_components`, `dash_core_components`, `dash_html_components`
et `numpy`

Sous Windows - Taper la commande : 
```bash
pip install -r requirements.txt
```
Puis lancer le programme avec 
```bash
python main.py
```

Sous Linux - Taper la commande : 
```bash
python3 -m pip install -r requirements.txt
```
Puis lancer le programme avec 
```bash
python3 main.py
```
5. Naviguer vers http://127.0.0.1:8050/

## Developer Guide

Après avoir importer les différentes modules, le script commence par récupérer les données du sites avec 
un appel à la fonction `load_data_from_urls(*urls)` qui prend un nombre variable d'url en entrée. Si il n'existe
pas encore de dossier "CSVFiles", le module `requests` est utilisé pour télécharger et extraire les données dans le
répertoire "CSVFiles".  
  
Ensuite, on récupère la liste des noms des fichiers avec la fonction `get_csv_files()` pour pouvoir le passer en paramètre de
`get_dataframe(csv_files)` pour générer le dataframe qui sera utiliser pour le reste du programme. Après avoir lu chaque csv,
les pays qui seront présent dans le nouveau dataframe sont filtré en amont. Pour ne garder que les pays unique, et non certains ensembles
de pays tels que les rassemblement de continents ou les unions de plusieurs pays, tous les pays contenant l'un des mots suivant est enlevé des
pays à parcourir : `"&", "dividend", "IBRD", "OECD", "World", "America", "Africa", "Asia", "Aruba",
                    "Europe", "IDA", "Euro", "Fragile"`  
Le nouveau dataframe possède 12825 lignes et 9 colonnes, qui sont les suivantes :
- 'Country Name'
- 'Country Code'
- 'Year'
- 'CO2 emissions (kt)'
- 'CO2 emissions (metric tons per capita)'
- 'CO2 emissions (kg per PPP $ of GDP)'
- 'Total CO2 emissions (kt)'
- 'Total CO2 emissions (metric tons per capita)'
- 'Total CO2 emissions (kg per PPP $ of GDP)'
  
Ces colonnes sont associés aux différentes listes de données qui ont été rempli en itérant sur chaque pays et chaque années.
Les colonnes représentant les émissions totales represente le nombre total d'émissions émis dans les années d'avant : la données représentant
le nombre total d'émissions émissions en 1980 prend la valeur de la somme de toutes les lignes d'avant.
Ceci permet d'avoir les informations des émissions émissions émise lors d'une certaines périodes

Finalement, le dashboard peut être lancé avec `dashboard(data)`. Ici les différentes fonctions pour créer les graphiques sont appelées : 
* create_scatter(data, selected_country) : Cette fonction prend les données et un pays en paramètre et retourne un graphique en nuage de points
sur les émissions par années du pays en particulier.
* create_global_histogram(data, years_range) : Cette fonction p
* create_income_histogram(data, years_range)
* create_choropleth_map(data, years_range, log_view, data_filter)
* create_pie_chart(data, years_range, data_filter)

## Rapport d'analyse
