import requests
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Fetch list of countries from API
def get_countries():
    url = "https://disease.sh/v3/covid-19/countries"
    res = requests.get(url).json()
    return sorted([country['country'] for country in res])

app = dash.Dash(__name__)
app.title = "🌐 COVID-19 Live Dashboard"

app.layout = html.Div([
    html.H1("COVID-19 Tracker", style={'textAlign': 'center'}),
    
    html.Label("Select Country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in get_countries()],
        value='India'
    ),
    dcc.Graph(id='covid-graph'),
    html.Div(id='live-text', style={'marginTop': 20, 'textAlign': 'center'}),
])
