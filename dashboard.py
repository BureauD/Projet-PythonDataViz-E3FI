# filename = 'dash-01.py'

#
# Imports
#

import plotly_express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

#
# Data
#

year = 2002

gapminder = px.data.gapminder() # (1)
print(gapminder)
years = gapminder["year"].unique()
data = { year:gapminder.query("year == @year") for year in years} # (2)
print(data)
#
# Main
#

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)


    app.layout = html.Div(children=[

                            html.H1(children=f'Life expectancy vs GDP per capita ({year})',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Div(children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year {year}. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            '''), # (7)

    ]
    )

    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)