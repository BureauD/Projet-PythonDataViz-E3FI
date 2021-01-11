import pandas as pd
import plotly.graph_objs as go
import plotly

df = pd.read_csv('CSVFiles/gapminder.csv')

years = df['year']

continents = df['continent']

continents = continents.unique()

year = 1992
continent = 'Asia'
asia1992 = df.query("continent=='Asia' and year==1992")


trace = go.Scatter(
     x=asia1992['mortality'],
     y=asia1992['fertility'],
     mode='markers',
     )
print(asia1992['mortality'])
data = [trace]
layout = go.Layout(title='Asia : fertility vs mortality (1992)',
                     xaxis=dict(
                         title='mortality',
                         ticklen=5,
                         zeroline=False,
                         gridwidth=2,
                     ),
                     yaxis=dict(
                         title='fertility',
                         ticklen=5,
                         zeroline=False,
                         gridwidth=2,
                     ),)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='fig.html', auto_open=False, include_plotlyjs='cdn')

def plot_from_file(filename):
    
    replace_text_in_file(filename,"Country Name", "Country")
    replace_text_in_file(filename,"'","")

    df = pd.read_csv(filename,error_bad_lines=False,encoding='utf-8')
    
    print(df.describe())
    print(df.nunique)

    countries = df['Country']
    countries = countries.unique()
    print(countries)

    #france = df.query("Country=='France'")
    """ for country_name in countries:
        print(country_name)
        #normalized_string = unidecode.unidecode(country_name)
        country = df.query("Country=='"+country_name+"'")
        print(country)
        years = country['Year'].unique()
        print(years)
        emissions = country['Total CO2 Emissions Excluding Land-Use Change and Forestry (MtCO2)'].unique()
        print(emissions)
        try:
            trace(country_name,years,emissions)
        except SyntaxError:
            print("SyntaxError : "+country) """

    for country_name in countries:
        try:
            trace(country_name,get_values_from_countries(df,country_name))
        except SyntaxError:
            print("SyntaxError : "+country_name)

    #france = get_values_from_countries(df,'France')
    #trace('France',france)

    # chine = getValuesFromCountry(df,'Chine')
    # trace('Chine',chine)

    # japon = getValuesFromCountry(df,'Japon')
    # trace('Japon',japon)

def trace(country_name, country):
    
    trace = go.Scatter(
        x= tuple(country.keys()),
        y= tuple(country.values()),
        mode='markers',
        )

    data = [trace]
    layout = go.Layout(title= country_name + ' : Total CO2 Emissions Excluding Land-Use Change and Forestry (MtCO2) per year',
                        xaxis=dict(
                            title='Years',
                            ticklen=5,
                            zeroline=False,
                            gridwidth=2,
                        ),
                        yaxis=dict(
                            title='Total CO2 Emissions Excluding Land-Use Change and Forestry (MtCO2)',
                            ticklen=5,
                            zeroline=False,
                            gridwidth=2,
                        ),)
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='Output/Emissions_'+country_name+'.html', auto_open=False, include_plotlyjs='cdn')   

    def replace_text_in_file(filename, old, new):
        """Multiplication de deux nombres entiers.

        Cette fonction ne sert pas à grand chose.

        Parameters
        ----------
        nombre1 : int
            Le premier nombre entier.
        nombre2 : int
            Le second nombre entier.

            Avec une description plus longue.
            Sur plusieurs lignes.

        Returns
        -------
        int
            Le produit des deux nombres.
        """
        text = open(filename, "r")
        text = ''.join([i for i in text]).replace(old, new)
        file = open(filename, "w")
        file.writelines(text)
        file.close()
    #url = 'https://static.data.gouv.fr/resources/cait-country-greenhouse-gas-emissions-data/20160831-154808/caitcountryghgemissions-csv0.zip'
