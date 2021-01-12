# Imports
import pandas as pd
import plotly.graph_objs as go
import plotly
import plotly_express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import csv
import requests
import zipfile
import io
import fileinput
import re
import numpy as np

# Static values
CSV_FILES_PATH = os.path.abspath(os.path.join(os.getcwd(),"CSVFiles"))
CSV_FILE_EMISSION_PER_COUNTRY = ""
CSV_FILE_EMISSION_PER_CAPITA = ""
CSV_FILE_EMISSION_PER_INCOME = ""
CSV_FILES = []


def load_data_from_urls(*urls):
    """Load data from multiple urls.

    The data is loaded in CSVFiles directory inside the project's directory.

    Parameters
    ----------
    urls : string
        Websites's url to download data from.
    """
    for url in urls:
        response = requests.get(url, stream=True)
        content = io.BytesIO(response.content)
        with zipfile.ZipFile(content) as zip_ref:
            for zip_info in zip_ref.infolist():
                zip_info.filename = os.path.basename(zip_info.filename).replace(" ", "")
                try:
                    zip_ref.extract(zip_info, CSV_FILES_PATH)
                except PermissionError:
                    print("Files already downloaded")


def get_csv_files():
    """Get files's name and store them in global variable.
    """
    # Global variable to get
    global CSV_FILE_EMISSION_PER_COUNTRY
    global CSV_FILE_EMISSION_PER_CAPITA
    global CSV_FILE_EMISSION_PER_INCOME
    global CSV_FILES

    # Look for file
    for filename in os.listdir(CSV_FILES_PATH):
        #replace_text_in_file(file_path, "Country Name", "Country")
        #replace_text_in_file(file_path, "'", "")
        if(re.match(r"API_EN.ATM.CO2E.KT_DS2_.*._csv_v2_.*.csv", filename)):
            CSV_FILE_EMISSION_PER_COUNTRY = filename
            CSV_FILES.append(CSV_FILE_EMISSION_PER_COUNTRY)
        elif(re.match(r"API_EN.ATM.CO2E.PC_DS2_.*._csv_v2_.*.csv", filename)):
            CSV_FILE_EMISSION_PER_CAPITA = filename
            CSV_FILES.append(CSV_FILE_EMISSION_PER_CAPITA)
        elif(re.match(r"API_EN.ATM.CO2E.PP.GD_DS2_.*._csv_v2_.*.csv", filename)):
            CSV_FILE_EMISSION_PER_INCOME = filename
            CSV_FILES.append(CSV_FILE_EMISSION_PER_INCOME)
        

def get_dataframe():
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
    files = list()

    for file in CSV_FILES:
        path = os.path.join(CSV_FILES_PATH,file)
        df = pd.read_csv(path, encoding='utf-8', skiprows=4)
        files.append(df)

    # Get unique contries
    countries = files[0]['Country Name']
    countries = countries.unique()

    countries = files[0]['Country Name']
    countries = countries.unique()
    # Create year list
    years = list()
    for i in range(len(files[0].columns)-9):
        years.append(files[0].columns[i+4])

    countries_name_data = list()
    countries_code_data = list()
    years_data = list()

    emission_data = list()
    emissions_capita_data = list()
    emissions_income_data = list()

    total_emissions_data = list()
    total_emissions_capita_data = list()
    total_emissions_income_data = list()

    for country in countries:
        total_emission = 0
        total_emission_capita = 0
        total_emission_income = 0

        try:
            country_query_emissions = files[0].query("`Country Name`=='"+country+"'")
            country_query_capita = files[1].query("`Country Name`=='"+country+"'")
            country_query_income = files[2].query("`Country Name`=='"+country+"'")
        except SyntaxError:
            if(country == "Cote d'Ivoire"):
                country_query_emissions = files[0].query("`Country Code`=='CIV'")
                country_query_capita = files[1].query("`Country Code`=='CIV'")
                country_query_income = files[2].query("`Country Code`=='CIV'")
            
        for year in years:
            countries_name_data.append(country)
            countries_code_data.append(country_query_emissions["Country Code"].array[0])
            years_data.append(int(year))

            emission_data.append(country_query_emissions[year].array[0])
            emissions_capita_data.append(country_query_capita[year].array[0])
            emissions_income_data.append(country_query_income[year].array[0])

            total_emission += country_query_emissions[year].sum()
            total_emission_capita += country_query_capita[year].sum()
            total_emission_income += country_query_income[year].sum()

            total_emissions_data.append(total_emission)
            total_emissions_capita_data.append(total_emission_capita)
            total_emissions_income_data.append(total_emission_income)

    # Create panda dataframe
    data = pd.DataFrame({'Country Name': countries_name_data,
                         'Country Code': countries_code_data,
                         'Year': years_data,
                         'CO2 emissions (kt)': emission_data,
                         'CO2 emissions (metric tons per capita)': emissions_capita_data,
                         'CO2 emissions (kg per PPP $ of GDP)':emissions_income_data,
                         'Total CO2 emissions (kt)': total_emissions_data,
                         'Total CO2 emissions (metric tons per capita)': total_emissions_capita_data,
                         'Total CO2 emissions (kg per PPP $ of GDP)': total_emissions_income_data})

    return data


def create_histogram(data,years_range,data_filter):
    """Create histogram with data.

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
    range = [years_range[0]-1960,years_range[1]-1960]

    fig = plotly.subplots.make_subplots(rows=1, cols=1)
    if(data_filter == 'Global CO2 emissions per income (kt)'):
        income_types =  ['Low income', 'Lower middle income', 'Middle income', 'Upper middle income', 'High income']
        emissions_income = list()
        for income_type in income_types:
            query = data.query("`Country Name`=='"+income_type+"'")
            total_emission_array = query["Total CO2 emissions (kt)"].array
            emissions_income.append(total_emission_array[range[1]] - total_emission_array[range[0]])
        
        df = pd.DataFrame({'Income type':income_types,
                           'Total CO2 emissions (kt)':emissions_income})

        fig = px.histogram(df,x="Income type",y="Total CO2 emissions (kt)",
                                                nbins=5)

    else:
        fig = px.histogram(data, x="Year", y="CO2 emissions (kt)",
                                           nbins=12,
                                           range_x=[years_range[0], years_range[1]])

    return fig
                                    

def create_choropleth_map(data,years_range,log_values,data_filter):
    """Create figure of choropleth map with data.

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
    countries = data['Country Name']
    countries = countries.unique()
    
    countries_name = list()
    countries_code = list()
    total_CO2_emissions = list()
    range = [years_range[0]-1960,years_range[1]-1960]
    excluded_str = ["&","income","dividend","IBRD","OECD","World","America","Africa","Europe","Asia","Aruba"]

    for country in countries:
        if not any(str in country for str in excluded_str):
            try:
                country_query = data.query("`Country Name`=='"+country+"'")
            except SyntaxError:
                if(country == "Cote d'Ivoire"):
                    country_query = data.query("`Country Code`=='CIV'")
            total_emission_array = country_query[data_filter].array
            total_emission_in_range = total_emission_array[range[1]] - total_emission_array[range[0]] 
            total_CO2_emissions.append(total_emission_in_range) 
            countries_name.append(country_query['Country Name'].unique()[0])
            countries_code.append(country_query['Country Code'].unique()[0])

    if(log_values):
        np.seterr(divide='ignore')
        values = np.log10(total_CO2_emissions)
        prefix = "1.e"
    else:
        values = total_CO2_emissions
        prefix = ""

    fig = go.Figure(data=go.Choropleth(
        locations=countries_code,
        z=values,
        text=countries_name,
        autocolorscale=True,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix=prefix,
        colorbar_title=data_filter.replace("Total ","")
    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://databank.worldbank.org">\
                World Bank Data</a>',
            showarrow=False
        )],
    )

    return fig

def create_scatter(data,selected_country):
    countries = { country:data.query("`Country Name`== @country")
                  for country in data["Country Name"].unique()}

    fig = px.scatter(countries[selected_country], x="Year", y="CO2 emissions (kt)",
                                                  hover_name="Country Name")
    
    return fig

def create_pie_chart(data,years_range,data_filter):
    countries = data['Country Name']
    countries = countries.unique()

    if(data_filter == 'Total CO2 emissions (kt)'):
        other_countries_range = 10000000.00
    elif(data_filter == 'Total CO2 emissions (metric tons per capita)'):
        other_countries_range = 300.00
    else:
        other_countries_range = 10.00
    countries_name = list()
    other_countries_total_emissions = 0
    total_CO2_emissions = list()
    range = [years_range[0]-1960,years_range[1]-1960]
    excluded_str = ["&","income","dividend","IBRD","OECD","World","America","Africa","Europe","Asia","Aruba"]

    for country in countries:
        if not any(str in country for str in excluded_str):
            try:
                country_query = data.query("`Country Name`=='"+country+"'")
            except SyntaxError:
                if(country == "Cote d'Ivoire"):
                    country_query = data.query("`Country Code`=='CIV'")
            total_emission_array = country_query[data_filter].array
            total_emission_in_range = total_emission_array[range[1]] - total_emission_array[range[0]]
            if(total_emission_in_range <= other_countries_range):
                other_countries_total_emissions += total_emission_in_range
            else:
                total_CO2_emissions.append(total_emission_in_range) 
                countries_name.append(country_query['Country Name'].unique()[0])

    countries_name.append("Other countries")
    total_CO2_emissions.append(other_countries_total_emissions)

    fig = go.Figure(data=[go.Pie(labels=countries_name,values=total_CO2_emissions,
                                                       textposition='inside')])

    return fig

def dashboard(data):
    """Create interactive dashboard from csv file.

    Cette fonction ne sert pas à grand chose.

    Parameters
    ----------
    filename : string
        Name of the file to read.
    """
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    scatter = create_scatter(data,"France")

    histogram = create_histogram(data,years_range=[1960,2014],data_filter="Global CO2 emissions per income (kt)")

    map = create_choropleth_map(data,years_range=[1960,2016],log_values=False,data_filter="CO2 emissions (kt)")

    pie = create_pie_chart(data,years_range=[1960,2016],data_filter="CO2 emissions (kt)")

    app.layout = html.Div(children=[

                            html.Div([
                                html.H1(children=f'CO2 emissions per country',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),

                                dcc.Graph(
                                    id='map',
                                    figure=map
                                ),

                                dcc.Checklist(
                                    options=[
                                        {'label': 'Logarithmic view', 'value': 'log_view'}
                                    ],
                                    value=[],
                                    id='log_view_map'

                                ),

                                dcc.Dropdown(
                                    id='data_dropdown_map',
                                    options = [
                                        {'label': 'Total CO2 emissions (kt)', 'value': 'Total CO2 emissions (kt)'},
                                        {'label': 'Total CO2 emissions (metric tons per capita)', 'value': 'Total CO2 emissions (metric tons per capita)'},
                                        {'label': 'Total CO2 emissions (kg per PPP $ of GDP)', 'value': 'Total CO2 emissions (kg per PPP $ of GDP)'}
                                    ],
                                    value='Total CO2 emissions (kt)',
                                    multi=False,
                                    clearable=False,
                                    style={"width": "50%"}
                                ),

                                dcc.RangeSlider(
                                    id='year_slider_map',
                                    min=data['Year'].min(),
                                    max=2016,
                                    step=1,
                                    value=[data['Year'].min(),2016],
                                    dots=True,
                                    allowCross=False,
                                    marks = { str(year) : { 
                                        'label': str(year),
                                        'style': {'color':'#7fafdf'}
                                        } 
                                        for year in data["Year"].unique()}
                                ),
                                html.Div(id='output-container-range-slider-map'),


                                html.Div(children=f'''
                                    The graph above shows relationship between life expectancy and
                                    GDP per capita for year. Each continent data has its own
                                    colour and symbol size is proportionnal to country population.
                                    Mouse over for details.
                                '''),
                            ]),

                            html.Div([
                                html.H1(children=f'Global CO2 emissions',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),

                                dcc.Graph(
                                    id='histogram',
                                    figure=histogram
                                ),

                                dcc.Dropdown(
                                    id='data_dropdown_histogram',
                                    options = [
                                        {'label': 'Global CO2 emissions per year (kt)', 'value': 'Global CO2 emissions per year (kt)'},
                                        {'label': 'Global CO2 emissions per income (kt)', 'value': 'Global CO2 emissions per income (kt)'}
                                    ],
                                    value='Global CO2 emissions per year (kt)',
                                    multi=False,
                                    clearable=False,
                                    style={"width": "50%"}
                                ),

                                dcc.RangeSlider(
                                    id='year_slider_histogram',
                                    min=data['Year'].min(),
                                    max=2016,
                                    step=1,
                                    value=[data['Year'].min(),2015],
                                    dots=True,
                                    allowCross=False,
                                    marks = { str(year) : { 
                                        'label': str(year),
                                        'style': {'color':'#7fafdf'}
                                        } 
                                        for year in data["Year"].unique()}
                                ),
                                html.Div(id='output-container-range-slider-histogram'),

                                html.Div(children=f'''
                                    The graph above shows relationship between life expectancy and
                                    GDP per capita for year. Each continent data has its own
                                    colour and symbol size is proportionnal to country population.
                                    Mouse over for details.
                                '''),
                            ]),

                            html.Div([
                                html.H1(children=f'CO2 emissions (kt) per country',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),

                                dcc.Graph(
                                    id='pie',
                                    figure=pie
                                ),

                                dcc.Dropdown(
                                    id='data_dropdown_pie',
                                    options = [
                                        {'label': 'Total CO2 emissions (kt)', 'value': 'Total CO2 emissions (kt)'},
                                        {'label': 'Total CO2 emissions (metric tons per capita)', 'value': 'Total CO2 emissions (metric tons per capita)'},
                                        {'label': 'Total CO2 emissions (kg per PPP $ of GDP)', 'value': 'Total CO2 emissions (kg per PPP $ of GDP)'}
                                    ],
                                    value='Total CO2 emissions (kt)',
                                    multi=False,
                                    clearable=False,
                                    style={"width": "50%"}
                                ),

                                dcc.RangeSlider(
                                    id='year_slider_pie',
                                    min=data['Year'].min(),
                                    max=2016,
                                    step=1,
                                    value=[data['Year'].min(),2016],
                                    dots=True,
                                    allowCross=False,
                                    marks = { str(year) : { 
                                        'label': str(year),
                                        'style': {'color':'#7fafdf'}
                                        } 
                                        for year in data["Year"].unique()}
                                ),

                                html.Div(children=f'''
                                    The graph above shows relationship between life expectancy and
                                    GDP per capita for year. Each continent data has its own
                                    colour and symbol size is proportionnal to country population.
                                    Mouse over for details.
                                '''),
                            ]),

                            html.Div([
                                html.H1(children=f'CO2 emissions (kt) per country',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),

                                dcc.Graph(
                                    id='scatter',
                                    figure=scatter
                                ),

                                dcc.Dropdown(
                                    id='country_dropdown_scatter',
                                    options = [
                                        {'label': country, 'value': country}
                                        for country in data["Country Name"].unique()
                                    ],
                                    value='France',
                                    multi=False,
                                    clearable=False,
                                    style={"width": "50%"}
                                ),

                                html.Div(children=f'''
                                    The graph above shows relationship between life expectancy and
                                    GDP per capita for year. Each continent data has its own
                                    colour and symbol size is proportionnal to country population.
                                    Mouse over for details.
                                '''),
                            ])
    ]
    )
    @app.callback(
        #dash.dependencies.Output('output-container-range-slider', 'children'),
        dash.dependencies.Output('histogram', 'figure'),
        [dash.dependencies.Input('year_slider_histogram', 'value'),
        dash.dependencies.Input('data_dropdown_histogram', 'value')])
    def update_histogram(year_range,data_filter):
        return create_histogram(data,year_range,data_filter)

    @app.callback(
        #dash.dependencies.Output('output-container-range-slider', 'children'),
        dash.dependencies.Output('map', 'figure'),
        [dash.dependencies.Input('year_slider_map', 'value'),
        dash.dependencies.Input('log_view_map', 'value'),
        dash.dependencies.Input('data_dropdown_map', 'value')])
    def update_map(year_range,log_view,data_filter):
        return create_choropleth_map(data,year_range,log_view,data_filter)

    @app.callback(
        dash.dependencies.Output('scatter', 'figure'),
        [dash.dependencies.Input('country_dropdown_scatter', 'value')])
    def update_scatter(selected_country):
        return create_scatter(data,selected_country)

    @app.callback(
        dash.dependencies.Output('pie', 'figure'),
        [dash.dependencies.Input('year_slider_pie', 'value'),
        dash.dependencies.Input('data_dropdown_pie', 'value')])
    def update_pie(year_range,data_filter):
        return create_pie_chart(data,year_range,data_filter)

    app.run_server(debug=True)


def main():
    """Main function.

    Call the methods to set up the dashboard.
    """
    
    load_data_from_urls("http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=csv",
                        "http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=csv",
                        "http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PP.GD?downloadformat=csv")

    get_csv_files()

    data = get_dataframe()

    dashboard(data)


if __name__ == "__main__":
    main()
