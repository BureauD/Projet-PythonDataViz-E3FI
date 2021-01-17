# Projet-PythonDataViz-E3FI

 Ce projet permet de générer un dashboard interactif sur les émissions de CO2 dans le monde depuis 1960,
 en utilisant des fichiers au format .csv récupéré dynamiquement sur https://databank.worldbank.org/.  

 Le dashboard contient plusieurs graphiques sur les émissions totales de CO2 dans
 le monde, les émissions par habitants et également par rapport aux émissions
 en fonction du pouvoir d'achat relatif au PIB des différents pays.  
 
 Parmi ces graphiques, on y retrouve : 
 - Une carte du monde avec des données géolocalisées
 - Un diagramme circulaire
 - Un histogramme
 - Un diagramme à barre 
 - Un diagramme à point pour chaque pays
 
 
## User Guide:

1. Télécharger le projet depuis Github
2. Extraire le dossier
3. Naviguer dans le dossier depuis l'invite de commande Windows ou le terminal Linux
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

Après avoir importé les différents modules, le script commence par récupérer les données du site avec 
un appel à la fonction `load_data_from_urls(*urls)` qui prend un nombre variable d'url en entrée. S'il n'existe
pas encore de dossier "CSVFiles", le module `requests` est utilisé pour télécharger et extraire les données dans le
répertoire "CSVFiles".  
  
Ensuite, on récupère la liste des noms des fichiers avec la fonction `get_csv_files()` pour pouvoir le passer en paramètre de
`get_dataframe(csv_files)` pour générer le dataframe qui sera utiliser pour le reste du programme. Après avoir lu chaque csv,
les pays qui seront présents dans le nouveau dataframe sont filtré en amont. Pour ne garder que les pays uniques, et non certains ensembles
de pays tels que les rassemblement de continents ou les unions de plusieurs pays, tous les pays contenant l'un des mots suivant est enlevé des
pays à parcourir : `"&", "dividend", "IBRD", "OECD", "World", "America", "Africa", "Asia", "Aruba",
                    "Europe", "IDA", "Euro", "Fragile"`  
Le nouveau dataframe possède 12 825 lignes et 9 colonnes, qui sont les suivantes :
- 'Country Name'
- 'Country Code'
- 'Year'
- 'CO2 emissions (kt)'
- 'CO2 emissions (metric tons per capita)'
- 'CO2 emissions (kg per PPP $ of GDP)'
- 'Total CO2 emissions (kt)'
- 'Total CO2 emissions (metric tons per capita)'
- 'Total CO2 emissions (kg per PPP $ of GDP)'
  
Ces colonnes sont associées aux différentes listes de données qui ont été remplies en itérant sur chaque pays et chaque année.
Les colonnes représentant les émissions totales représentent le nombre total d'émissions émis dans les années d'avant : la donnée représentant
le nombre total d'émissions en 1980 prend la valeur de la somme de toutes les lignes d'avant.
Ceci permet d'avoir les informations des émissions émises lors d'une certaine période.  

Finalement, le dashboard peut être lancé avec `dashboard(data)`. Tout d'abord les données par rapport aux émissions selon le revenu sont séparées 
du dataframe principale pour ne pas fausser les données et seront seulement utilisé pour l'histogramme concerneant les revenus.
Ensuite, les différentes fonctions pour créer les graphiques sont appelées :
* `create_scatter(data, selected_country)` : Cette fonction prend les données et un pays en paramètre et retourne un graphique en nuage de points
sur les émissions par années du pays en particulier. Le graphique est créé grâce à la fonction `px.scatter()` du module `plotly_express`.
* `create_global_histogram(data, years_range)` : Cette fonction prend les données principale et réalise un histogramme simple sur 
les émissions globales de CO2 depuis 1960 jusqu'à 2016. Il y a en x les années et y les émissions, et chaque colonne représente une période 
de quatre années. Le graphique est créé grâce à la fonction `px.histogram()` du module `plotly_express`.
* `create_income_histogram(data, years_range)`: Cette fonction permet de créer un histogramme de 5 colonnes avec les données concernant le revenu
qui ont été séparées juste avant. Ce graphique permet de visualiser les émissions de chaque classe de revenu sur la période spécifié. Le graphique est créé grâce à la fonction `px.histogram()` du module `plotly_express`.
* `create_choropleth_map(data, years_range, log_view, data_filter)`: Cette fonction permet de créer la carte avec les données géolocalisées. 
La carte peut être affiché avec différentes données selon le paramètre `data_filter` qui représente le nom de la colonne dont l'on veut les données.
Il y a également un paramètre `log_view` qui permet d'afficher les données selon une échelle logarithmique. Le graphique est créé grâce à 
la fonction `go.Choropleth()` du module `plotly`.
* `create_pie_chart(data, years_range, data_filter)`: Cette fonction permet de créer le diagramme circulaire en fonctions des données 
spécifié par `data_filter`. Comme il y a un nombre élevé de pays à afficher et que un grand nombre de ces pays représente un pourcentage 
assez faible du total, les pays considérés en dessous d'un certain seuil sont rassemblé dans la catégorie `Other countries`. 
Le graphique est créé grâce à la fonction `go.Pie()` du module `plotly`.

## Rapport d'analyse
