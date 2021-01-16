# Projet-PythonDataViz-E3FI

 Ce projet permet de générer un dashboard interactif sur les émissions de CO2 dans le monde
 depuis des fichiers au format .csv récupérer dynamiquement sur https://databank.worldbank.org/.  

 Le dashboard contient plusieurs graphiques sur les émissions totales de CO2 dans
 le monde, les émissions par habitants et également par rapport au pouvoir d'achat
 relatif au PIB des différents pays.  
 
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



## Rapport d'analyse
