"""Dashboard app launcher.

This script gets data in csv format from WorldBank.org and uses
pandas module to read files and create a pandas.DataFrame with data
on registered CO2 emissions per country from 1960 to 2016.
It then create different figures and load a dashboard on
http://127.0.0.1:8050/

This script requires that `pandas`, `plotly`, `plotly_express`, `dash`,
`dash_bootstrap_components`, `dash_core_components`, `dash_html_components`
and `numpy` be installed within the Python environment you are running
this script in.

Author : Dimitri Bureau
"""

# Imports
import os
import zipfile
import io
import re
import requests
import pandas as pd
import plotly.graph_objs as go
import plotly
import plotly_express as px
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np

# Static values
CSV_FILES_PATH = os.path.abspath(os.path.join(os.getcwd(), "CSVFiles"))

def load_data_from_urls(*urls):
    """Load data from urls.

    Args:
        urls (String): Urls to download the data from
    """
    # Check if CSV files are already in folder
    if os.path.exists(CSV_FILES_PATH):
        print("Files already downloaded")
        return

    # Request download for each url and load data in CSVFiles
    for url in urls:
        response = requests.get(url, stream=True)
        content = io.BytesIO(response.content)
        with zipfile.ZipFile(content) as zip_ref:
            # Remove spaces and extract files from zip
            for zip_info in zip_ref.infolist():
                zip_info.filename = os.path.basename(zip_info.filename).replace(" ", "")
                try:
                    zip_ref.extract(zip_info, CSV_FILES_PATH)
                except PermissionError as pe:
                    print("PermissionError : "+pe)


def get_csv_files():
    """Get files's name and store them in global variable.

    Returns:
        List of String: Names of csv files
    """
    csv_files = list()
    # Find the csv files and store names in global variables
    for filename in os.listdir(CSV_FILES_PATH):
        if re.match(r"API_EN.ATM.CO2E.KT_DS2_.*._csv_v2_.*.csv", filename):
            csv_files.append(filename)
        elif re.match(r"API_EN.ATM.CO2E.PC_DS2_.*._csv_v2_.*.csv", filename):
            csv_files.append(filename)
        elif re.match(r"API_EN.ATM.CO2E.PP.GD_DS2_.*._csv_v2_.*.csv", filename):
            csv_files.append(filename)

    return csv_files


def get_country_from_data(data, country):
    """Return country's query from specified data.

    Args:
        data (pandas.DataFrame): Data to query from
        country (String): Country's name

    Returns:
        pandas.DataFrame: Country's query
    """
    try:
        country_query = data.query("`Country Name`=='"+country+"'")
    except SyntaxError:
        if country == "Cote d'Ivoire":
            country_query = data.query("`Country Code`=='CIV'")

    return country_query


def get_dataframe(csv_files):
    """Generate dataframe with data from files.

    Args:
        csv_files (List of String): Names of the files to read

    Returns:
        pandas.DataFrame: DataFrame for dashboard
    """
    # Read csv into dataframe for each files and store in list
    files = list()
    for file in csv_files:
        path = os.path.join(CSV_FILES_PATH, file)
        data = pd.read_csv(path, encoding='utf-8', skiprows=4)
        # Replace NaN values with 0.0 to avoid errors
        data.fillna(0.0, inplace=True)
        files.append(data)

    # Get unique contries
    countries = files[0]['Country Name']
    countries = countries.unique()
    excluded_str = ["&", "dividend", "IBRD", "OECD", "World", "America", "Africa", "Asia", "Aruba",
                    "Europe", "IDA", "Euro", "Fragile", "Middle income"]
    countries = [country for country in countries
                 if not any(str in country for str in excluded_str)]

    # Create year list
    year_columns = files[0].columns.values[4:-1]
    years = [year for year in year_columns
             if int(year) >= 1960 and int(year) <= 2016]

    # Countries info
    countries_name_data = list()
    countries_code_data = list()
    years_data = list()

    # Emissions info
    emission_data = list()
    emissions_capita_data = list()
    emissions_income_data = list()

    # Total emissions since first recorded year
    total_emissions_data = list()
    total_emissions_capita_data = list()
    total_emissions_income_data = list()

    # Append data for each country
    for country in countries:
        # Variable to compute total emissions
        total_emission, total_emission_capita, total_emission_income = 0, 0, 0

        # Query country for each file
        country_query_emissions = get_country_from_data(files[0], country)
        country_query_capita = get_country_from_data(files[1], country)
        country_query_income = get_country_from_data(files[2], country)

        # Append a line for each year for current country
        for year in years:
            countries_name_data.append(country)
            countries_code_data.append(country_query_emissions["Country Code"].array[0])
            years_data.append(int(year))

            emission_data.append(country_query_emissions[year].array[0])
            emissions_capita_data.append(country_query_capita[year].array[0])
            emissions_income_data.append(country_query_income[year].array[0])

            total_emission += country_query_emissions[year].array[0]
            total_emission_capita += country_query_capita[year].array[0]
            total_emission_income += country_query_income[year].array[0]

            total_emissions_data.append(total_emission)
            total_emissions_capita_data.append(total_emission_capita)
            total_emissions_income_data.append(total_emission_income)

    # Create pandas dataframe
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


def create_global_histogram(data, years_range):
    """Create histogram for global emissions.

    Args:
        data (pandas.DataFrame): Main dataframe for global emissions data
        years_range (List): List with starting and ending year on slider

    Returns:
        plotly.graph_objs._figure.Figure: Figure of global emissions histogram
    """
    # Global emissions histogram
    fig = px.histogram(data, x="Year", y="CO2 emissions (kt)",
                       range_x=[years_range[0], years_range[1]])

    # Set number of bins
    fig.update_traces(xbins=dict(
        start=1960,
        end=2016,
        size=4
    ))

    return fig


def create_income_histogram(data, years_range):
    """Create histogram on income data.

    Args:
        income_data (pandas.DataFrame): Dataframe on emissions based on income
        years_range (List): List with starting and ending year on slider

    Returns:
        plotly.graph_objs._figure.Figure: Figure of emissions based on income histogram
    """
    range = [years_range[0]-1960, years_range[1]-1960]
    income_types = ["Low income", "Lower middle income",
                    "Upper middle income", "High income"]

    # Histogram for emissions based on income class
    emissions_income = list()
    for income_type in income_types:
        query = data.query("`Country Name`=='"+income_type+"'")
        total_emission_array = query["Total CO2 emissions (kt)"].array
        emissions_income.append(total_emission_array[range[1]] - total_emission_array[range[0]])

    df = pd.DataFrame({'Income type': income_types,
                       'Total CO2 emissions (kt)': emissions_income})

    fig = px.histogram(df, x="Income type", y="Total CO2 emissions (kt)",
                       color_discrete_sequence=px.colors.qualitative.Vivid,
                       nbins=4)

    return fig


def create_choropleth_map(data, years_range, log_view, data_filter):
    """Create choropleth map.

    Args:
        data (pandas.DataFrame): Dataframe for global emissions data
        years_range (List): List with starting and ending year on slider
        log_view (Boolean): Value from checkbox to display Logarithmic values or not
        data_filter (String): Value from dropdown menu to select data to display

    Returns:
        plotly.graph_objs._figure.Figure: Figure of map
    """
    countries = data['Country Name']
    countries = countries.unique()
    countries_name = list()
    countries_code = list()
    total_CO2_emissions = list()
    range = [years_range[0]-1960, years_range[1]-1960]

    # Get countries's name, code and emissions in the specified year period
    for country in countries:
        country_query = get_country_from_data(data, country)
        total_emission_array = country_query[data_filter].array
        total_emission_in_range = total_emission_array[range[1]] - total_emission_array[range[0]]
        total_CO2_emissions.append(total_emission_in_range)
        countries_name.append(country_query['Country Name'].unique()[0])
        countries_code.append(country_query['Country Code'].unique()[0])

    # Display with a logarithmic scale if log_view is specified to True
    if log_view:
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
        colorbar_title=data_filter.replace("Total ", "")
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
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    return fig


def create_scatter(data, selected_country):
    """Create simple scatter with data from country.

    Args:
        data (pandas.DataFrame): Dataframe for global emissions data
        selected_country (String): Name of selected country

    Returns:
        plotly.graph_objs._figure.Figure: Figure of map
    """
    # Query countries
    countries = {country:data.query("`Country Name`== @country")
                 for country in data["Country Name"].unique()}

    fig = px.scatter(countries[selected_country], x="Year", y="CO2 emissions (kt)",
                     hover_name="Country Name")

    return fig


def create_pie_chart(data, years_range, data_filter):
    """Create pie chart with specified data.

    Args:
        data (pandas.DataFrame): Dataframe for global emissions data
        years_range (List): List with starting and ending year on slider
        data_filter (String): Value from dropdown menu to select pie chart

    Returns:
        plotly.graph_objs._figure.Figure: Figure of map
    """
    countries = data['Country Name']
    countries = countries.unique()

    # Find under which range countries fall into "Other countries" category
    if data_filter == 'Total CO2 emissions (kt)':
        other_countries_range = 10000000.00
    elif data_filter == 'Total CO2 emissions (metric tons per capita)':
        other_countries_range = 300.00
    else:
        other_countries_range = 10.00

    countries_name = list()
    other_countries_total_emissions = 0
    total_CO2_emissions = list()
    range = [years_range[0]-1960, years_range[1]-1960]

    # Get emissions from country during time period
    for country in countries:
        country_query = get_country_from_data(data, country)
        total_emission_array = country_query[data_filter].array
        total_emission_in_range = total_emission_array[range[1]] - total_emission_array[range[0]]
        if total_emission_in_range <= other_countries_range:
            other_countries_total_emissions += total_emission_in_range
        else:
            total_CO2_emissions.append(total_emission_in_range)
            countries_name.append(country_query['Country Name'].unique()[0])

    # Add the "Other countries" category
    countries_name.append("Other countries (less than {})".format(other_countries_range))
    total_CO2_emissions.append(other_countries_total_emissions)

    fig = go.Figure(data=[go.Pie(labels=countries_name,
                                 values=total_CO2_emissions,
                                 textposition='inside')])

    return fig


def dashboard(data):
    """Create interactive dashboard from DataFrame.

    Args:
        data (pandas.DataFrame): Dataframe for global emissions data
    """

    # Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Separate income data from main data
    countries = data['Country Name']
    countries_income = ["Low income", "Lower middle income",
                        "Middle income", "Upper middle income", "High income"]
    countries_no_income = [country for country in countries if 'income' not in country]
    income_data = data[~data['Country Name'].isin(countries_no_income)]
    data = data[~data['Country Name'].isin(countries_income)]

    # Create each figure
    scatter = create_scatter(data, "France")
    global_histogram = create_global_histogram(data, years_range=[1960, 2016])
    income_histogram = create_income_histogram(income_data, years_range=[1960, 2016])
    map = create_choropleth_map(data, years_range=[1960, 2016], log_view=False,
                                data_filter="Total CO2 emissions (kt)")
    pie = create_pie_chart(data, years_range=[1960, 2016], data_filter="CO2 emissions (kt)")

    # Set app layout
    app.layout = html.Div(children=[
        # First row with map and pie chart
        html.Div([
            html.H1(children='CO2 emissions per country',
                    style={'textAlign': 'center', 'color': '#7FDBFF'}),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id='map',
                            figure=map
                        ), md=8
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='pie',
                            figure=pie
                        ), md=4
                    ),
                ]
            ),

            # Logarithmiv view checklist
            dcc.Checklist(
                options=[
                    {'label': 'Logarithmic view',
                     'value': 'log_view'}
                ],
                value=[],
                id='log_view_map'
            ),

            # Data filter dropdown
            dcc.Dropdown(
                id='data_dropdown_first_row',
                options=[
                    {'label': 'Total CO2 emissions (kt)',
                     'value': 'Total CO2 emissions (kt)'},
                    {'label': 'Total CO2 emissions (metric tons per capita)',
                     'value': 'Total CO2 emissions (metric tons per capita)'},
                    {'label': 'Total CO2 emissions (kg per PPP $ of GDP)',
                     'value': 'Total CO2 emissions (kg per PPP $ of GDP)'}
                ],
                value='Total CO2 emissions (kt)',
                multi=False,
                clearable=False,
                style={"width": "50%"}
            ),

            # Range slider for time period
            dcc.RangeSlider(
                id='year_slider_first_row',
                min=data['Year'].min(),
                max=data['Year'].max(),
                step=1,
                value=[data['Year'].min(), data['Year'].max()],
                dots=True,
                allowCross=False,
                marks={str(year) : {
                    'label': str(year),
                    'style': {'color':'#7fafdf'}
                    }
                       for year in data["Year"].unique()}
            ),

            html.Div(children=[
                '''The first graph on the left shows CO2 emissions for every country in the world.
                The view can be changed to a logarithmic scale.''',
                html.Br(),
                '''The second graph is a pie chart reprensenting the percentage
                of emissions per country.''',
                html.Br(),
                html.Br(),
                '''The time period in which the CO2 emissions occured can be changed with the
                range slider. Data filters can be selected to show total emissions in kilotons,
                metric tons per capita or in kilograms per percentage of purchasing power parity
                for country's gross domestic product (PPP for GDP).
                Mouse over for details.'''
            ])
        ]),

        # Second row for global histogram and histogram based on income
        html.Div([
            html.H1(children='Global CO2 emissions (kt) and emissions per income class',
                    style={'textAlign': 'center', 'color': '#7FDBFF'}),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id='global_histogram',
                            figure=global_histogram
                        ), md=8
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='income_histogram',
                            figure=income_histogram
                        ), md=4
                    ),
                ]
            ),

            # Range slider for time period
            dcc.RangeSlider(
                id='year_slider_histogram',
                min=data['Year'].min(),
                max=data['Year'].max(),
                step=1,
                value=[data['Year'].min(), data['Year'].max()],
                dots=True,
                allowCross=False,
                marks={str(year): {
                    'label': str(year),
                    'style': {'color': '#7fafdf'}
                    }
                       for year in data["Year"].unique()}
            ),

            html.Div(children=[
                '''The first graph on the left is an histogram that hows global CO2 emissions
                in selected time period.The second graph represents the sum of emissions depending
                on income.''',
                html.Br(),
                '''The time period in which the CO2 emissions occured can be changed with the
                range slider.
                Mouse over for details.'''
            ])
        ]),

        # Third row with scatter for selected country
        html.Div([
            html.H1(children='CO2 emissions (kt) per country',
                    style={'textAlign': 'center', 'color': '#7FDBFF'}),

            # Dropdown to select country
            dcc.Dropdown(
                id='country_dropdown_scatter',
                options=[
                    {'label': country, 'value': country}
                    for country in data["Country Name"].unique()
                ],
                value='France',
                multi=False,
                clearable=False,
                style={"width": "50%"}
            ),

            dcc.Graph(
                id='scatter',
                figure=scatter
            ),

            html.Div(children=[
                '''This graph scatters a plot with registered CO2 emissions from 1960
                to 2016 based on selected country.'''
                ])
            ])
        ]
    )

    # Setting app callbacks for updating figures
    @app.callback(
        dash.dependencies.Output('map', 'figure'),
        dash.dependencies.Output('pie', 'figure'),
        [dash.dependencies.Input('year_slider_first_row', 'value'),
         dash.dependencies.Input('log_view_map', 'value'),
         dash.dependencies.Input('data_dropdown_first_row', 'value')])
    def update_first_row(year_range, log_view, data_filter):
        map = create_choropleth_map(data, year_range, log_view, data_filter)
        pie = create_pie_chart(data, year_range, data_filter)
        return map, pie

    @app.callback(
        dash.dependencies.Output('global_histogram', 'figure'),
        dash.dependencies.Output('income_histogram', 'figure'),
        [dash.dependencies.Input('year_slider_histogram', 'value')])
    def update_second_row(year_range):
        global_histogram = create_global_histogram(data, year_range)
        income_histogram = create_income_histogram(income_data, year_range)
        return global_histogram, income_histogram

    @app.callback(
        dash.dependencies.Output('scatter', 'figure'),
        [dash.dependencies.Input('country_dropdown_scatter', 'value')])
    def update_scatter(selected_country):
        return create_scatter(data, selected_country)

    # Run app
    app.run_server(debug=True)


def main():
    """Do main.

    Call the methods to set up the dashboard.
    """
    # Load the data from worldbank.org
    worldbank_url = "http://api.worldbank.org/v2/en/indicator/"
    load_data_from_urls(worldbank_url+"EN.ATM.CO2E.KT?downloadformat=csv",
                        worldbank_url+"EN.ATM.CO2E.PC?downloadformat=csv",
                        worldbank_url+"EN.ATM.CO2E.PP.GD?downloadformat=csv")

    # Find the downloaded csv files names and load into list
    csv_files = get_csv_files()

    # Create a panda dataframe for the dashboard to use
    data = get_dataframe(csv_files)

    # Set up the dashboard with the data
    dashboard(data)


if __name__ == "__main__":
    main()
