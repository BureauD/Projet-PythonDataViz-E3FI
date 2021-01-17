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
 
 De plus, chaque graphique possède un ou plusieurs éléments interactifs permettant de visualiser différentes données sur différentes périodes.
 
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

Tout les graphiques nécessaires au dashboard sont maintenant prêt, et on peut les ajouter à l'app qui a été créée tels que `app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])`. L'app utilise le module `dash_bootstrap_components` pour bien organiser les graphiques sur la page en terme de lignes (`dbc.Row`) et de colonnes (`dbc.Col`), l'organisation de la page étant définie dans la fonction `app.layout()`. Ce layout possèdent trois conteneur `html.Div` : 
- Le premier contient la carte et le diagramme circulaire. Il y a également un curseur pour sélectionner la période sur laquelle on veut les données et un menu de sélection pour choisir quel type de données on veut. Pour la carte, il y a également une case à cocher pour utiliser l'échelle logarithmique ou non.
- Le second contient l'histogramme des émissions globales au cours du temps et l'histogramme en fonction des revenus. Comme précédemment, il y a un curseur pour sélectionner la période sur laquelle on veut les données.
- Le dernier contient seulement le diagramme à point et un menu de sélection pour choisir le pays.  

Il faut également mettre à jour les graphiques lorsque que les différents menus de sélection et autres éléments interactifs correspondant sont changé. Pour cela, il faut créer trois fonctions, une pour chaque conteneur, avec le décorateur `app.callback(dash.dependencies.Output(),dash.dependencies.Input())` devant les fonctions. Pour chaque fonction, la ou les sorties sont les différents graphiques associés au conteneur et les entrées sont les valeurs des éléments interactifs. Les fonctions peuvent ainsi appeler les fonctions qui créent le graphique approprié avec les nouveaux paramètres pour actualiser la page.  

Pour finir, l'app est lancée avec `app.run_server(debug=True)` et le dashboard est prêt à l'utilisation.

## Rapport d'analyse

En analysant les données du dashboard on peut faire différents constats par rapport aux émissions de globales de CO2 et qui sont les plus grands émetteurs de CO2. Les différentes données sont exprimées soit en kilotonnes, en tonnes par habitants ou en kilogramms par parité du pouvoir d'achat relatif au produit intérieur brut.

![FirstRow](https://user-images.githubusercontent.com/50491971/104844887-ee573080-58d2-11eb-883b-aaa11a6d9314.PNG)

Si on prend la carte et le diagramme circulaire des émissions depuis 1960, on remarque 3 pays qui sortent du lot : les Etats-Unis, la Chine, et la Russie anciennement URSS. En effet, on remarque qu'à eux seuls, ces pays ont émis 51.1 % des émissions de CO2 soit plus de la moitié des émissions totales dans le monde.
On remarque également que d'autres pays d'Asie tel que l'Inde ou le Japon, ou d'Europe avec la France ou l'Allemagne représentent également un pourcentage conséquent, mais bien loin des trois plus gros pays. On remarque également que presque 80 % des émissions globales ont été émises par à peine une vingtaine de pays.

De plus, même parmi les 3 premiers, il existe de grands écarts : les Etats-Unis sont loin devant avec 270 M de kilotonnes de CO2 émises sur cette période, la Chine est en seconde place avec 189 M et la Russie avec 132 M. Pourtant si on regarde seulement entre 2000 et 2016, on fait un constat bien différent, car la Chine est à présent numéro 1 avec 120M d'émissions, les Etats-Unis deuxième avec 87M et la Russie troisième avec près de 27M, presque à égalité avec l'Inde. Ces 3 pays représentent à présent 48.54 % des émissions totales, comme on peut le voir ci-dessous : 

![FirstRow2000-2016](https://user-images.githubusercontent.com/50491971/104846712-34fd5880-58dc-11eb-942b-53eae07b8bd2.PNG)

À l'inverse, si on regarde les graphiques sur la période de 1960 à 2000, les Etats-Unis reprennent la première place avec 170 M, la Russie/URSS est deuxième avec 105 M et la Chine se trouve à 68 M. En effet, ces écarts reflète un monde en pleine guerre froide et d'une Chine pas encore complétement industrialisé. En effet, les Etats-Unis et l'URSS représentaient à eux seuls 42.8 % des émissions et les pays à moins de 10 M d'émission au total représentaient 26.8 % des émissions.

![FirstRow1960-2000](https://user-images.githubusercontent.com/50491971/104846715-36c71c00-58dc-11eb-812a-fc66b6b37db2.PNG) 


Si on regarde de plus près les courbes d'émission pour les Etats-Unis, la Russie/URSS et la Chine, on remarque bien la même chose et quelques autres détails importants. 
![UnitedStates](https://user-images.githubusercontent.com/50491971/104846717-3a5aa300-58dc-11eb-8b39-29a2fedcd37c.PNG)
![RussianFederation](https://user-images.githubusercontent.com/50491971/104846718-3af33980-58dc-11eb-8d5a-cee4c8b8ed24.PNG)
![China](https://user-images.githubusercontent.com/50491971/104846723-3c246680-58dc-11eb-8a7e-1fcf5ad8ad22.PNG) 

Pour les Etats-Unis, on remarque une croissance importante et constante, avec des émissions de CO2 qui vont de 3 M à presque 6 M par an, jusqu'à la crise financière de 2007-2008 qui marque la fin de cette croissance, qui maintenant baisse faiblement. 

Pour l'URSS, on remarque une évolution similaire lors de la guerre froide avec une croissance des émissions de 1.5 M en 1960 à presque 4 M au plus haut, en 1988. On constate un déclin jusqu'à la chute de l'URSS en 1991 qu'il est très important. En effet, bien que les émissions passent de 3.5 M en 1991 à 2 M en 1992, ceci est dû à la séparation entre les différents membres de l'URSS et la Russie. Malgré tout, il y a tout de même une baisse des émissions jusqu'en 1998 où la Russie retombe au même niveau d'émissions que l'URSS en 1960. Après les années 2000, la Russie se maintient entre 1.5 M de 2 M d'émissions par ans. 

Pour la Chine, son niveau d'émission se trouve à 780 k en 1960 et est toujours au même niveau en 1970. À partir de ce moment, les émissions de la Chine comment à augmenter faiblement pour dépasser 1 M en 1975, 2 M en 1986 et 3M en 1994 pour se retrouver à 3.4 M en 2000. La Chine a ensuite une augmentation vertigineuse de ses émissions de CO2 et comptabilise plus de 10.2 M de kilotonnes de CO2 émises en 2013 et 2014. Les émissions commencent à faiblir lentement à partir de ce moment, mais on remarque tout de même une moyenne de 10 M d'émissions entre 2011 et 2016.



