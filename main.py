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

def get_values_from_countries(file,countryName):
    country = file.query("Country=='"+countryName+"'")
    values = dict()
    for i in range(len(file.columns)-5):
        values[(str)(1960+i)] = country[(str)(1960+i)].array[0]
    return values

def plot_from_file(filename):
    
    df = pd.read_csv(filename,error_bad_lines=False,encoding='ISO-8859-1',skiprows=1)
    print(df.describe())
    print(df.nunique)

    countries = df['Country']
    countries = countries.unique()
    print(countries)

    #france = df.query("Country=='France'")

    for country_name in countries:
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
            print("SyntaxError : "+country)

    # france = getValuesFromCountry(df,'France')
    # trace('France',france)

    # chine = getValuesFromCountry(df,'Chine')
    # trace('Chine',chine)

    # japon = getValuesFromCountry(df,'Japon')
    # trace('Japon',japon)

def trace(countryName, years, emissions):
    
    trace = go.Scatter(
        x= years,
        y= emissions,
        mode='markers',
        )

    data = [trace]
    layout = go.Layout(title= countryName + ' : Total CO2 Emissions Excluding Land-Use Change and Forestry (MtCO2) per year',
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
    plotly.offline.plot(fig, filename='Output/Emissions_'+countryName+'.html', auto_open=False, include_plotlyjs='cdn')   

def load_data_from_web():
    #Download files from web
    csv_files_path = "C:/Users/Dimitri/Desktop/ProjetPython/CSVFiles"
    url = 'https://static.data.gouv.fr/resources/cait-country-greenhouse-gas-emissions-data/20160831-154808/caitcountryghgemissions-csv0.zip'
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
    df = pd.read_csv(filename,error_bad_lines=False,encoding='ISO-8859-1',skiprows=1)

    countries = df['Country']
    countries = countries.unique()

    france = df.query("Country=='France'")
    years = france['Year'].unique()
    data = { Year:france.query("Year == @Year") for Year in years}
    emissions = france['Total CO2 Emissions Excluding Land-Use Change and Forestry (MtCO2)'].unique()

    app = dash.Dash(__name__) # (3)

    for year in years:
        fig = px.scatter(data[year], x="Year", y="Total CO2 Emissions Excluding Land-Use Change and Forestry (MtCO2)",
                            
                            size="Year",
                            hover_name="Country") # (4)


    app.layout = html.Div(children=[

                            html.H1(children=f'Total CO2 Emissions Excluding Land-Use Change and Forestry (MtCO2) per Year ',
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
    
    load_data_from_web()
    dashboard('CSVFiles/CAITCountryCO2Emissions.csv')
    #plot_from_file('CSVFiles/CAITCountryCO2Emissions.csv')

if __name__ == "__main__":
    main()