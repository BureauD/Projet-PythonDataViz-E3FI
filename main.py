import pandas as pd
import plotly.graph_objs as go
import plotly
import plotly_express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import unidecode
import os
import csv
import requests
import zipfile
import io
import fileinput

def get_values_from_countries(file,countryName):
    country = file.query("Country=='"+countryName+"'")
    values = dict()
    for i in range(len(file.columns)-5):
        values[(str)(1960+i)] = country[(str)(1960+i)].array[0]
    return values

def replace_text_in_file(filename,old,new):
    text = open(filename, "r")
    text = ''.join([i for i in text]) \
    .replace(old,new)
    file = open(filename,"w")
    file.writelines(text)
    file.close()


def plot_from_file(filename):
    
    replace_text_in_file(filename,"Country Name", "Country")
    replace_text_in_file(filename,"'","")

    df = pd.read_csv(filename,error_bad_lines=False,encoding='utf-8',skiprows=4)
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

def load_data_from_url(url):
    #Download files from web
    csv_files_path = "C:/Users/Dimitri/Desktop/ProjetPython/CSVFiles"
    #url = 'https://static.data.gouv.fr/resources/cait-country-greenhouse-gas-emissions-data/20160831-154808/caitcountryghgemissions-csv0.zip'
    
    response = requests.get(url,stream=True)

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        print(zip_ref.namelist())
        for zip_info in zip_ref.infolist():
            print(os.path.basename(zip_info.filename).replace(" ",""))
            zip_info.filename = os.path.basename(zip_info.filename).replace(" ","")
            try:
                zip_ref.extract(zip_info,csv_files_path)   
            except PermissionError:
                print("Files already downloaded")     


def dashboard(filename):

    replace_text_in_file(filename,"Country Name", "Country")
    replace_text_in_file(filename,"'","")

    df = pd.read_csv(filename,error_bad_lines=False,encoding='utf-8',skiprows=4)
    print(df)
    countries = df['Country']
    countries = countries.unique()
    test = df.query("Country=='France'")
    print(test)
    """ for i in range(len(df.columns)-5):
        values[(str)(1960+i)] = country[(str)(1960+i)].array[0] """

    france = get_values_from_countries(df,'France')
    years = france.keys()
    emissions = france.values()

    countries_data = list()
    years_data = list()
    emission_data = list()

    for country in countries:
        country_query = df.query("Country=='"+country+"'")
        for year in years:
            countries_data.append(country)
            years_data.append(year)
            emission_data.append(country_query[year].array[0])

    #Remplace le dict
    data = pd.DataFrame({'Country': countries_data,
                         'Year': years_data,
                         'Émissions de CO2 (kt)': emission_data})
    print(data)

    show_data_countries = { country:data.query("Country == @country") for country in countries}
    show_data_years = { year:data.query("Year == @year") for year in years}

    """ france = df.query("Country=='France'")
    years = france['Year'].unique()
    data = { Year:france.query("Year == @Year") for Year in years}
    emissions = france['Total CO2 Emissions Excluding Land-Use Change and Forestry (MtCO2)'].unique() """

    app = dash.Dash(__name__) # (3)

    fig = px.scatter(data, x="Year", y="Émissions de CO2 (kt)",
                        hover_name="Country"
                        ) # (4)

    app.layout = html.Div(children=[

                            html.H1(children=f'Émissions de CO2 (kt) par années',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Div(children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            '''), # (7)

    ]
    )

    app.run_server(debug=True) # (8)

def main():
    
    #load_data_from_url("http://api.worldbank.org/v2/fr/indicator/EN.ATM.CO2E.KT?downloadformat=csv")
    #load_data_from_url("http://api.worldbank.org/v2/fr/indicator/EN.ATM.CO2E.PC?downloadformat=csv")
    dashboard('CSVFiles/API_EN.ATM.CO2E.KT_DS2_fr_csv_v2_1754986.csv')
    #plot_from_file('CSVFiles/API_EN.ATM.CO2E.KT_DS2_fr_csv_v2_1754986.csv')


if __name__ == "__main__":
    main()