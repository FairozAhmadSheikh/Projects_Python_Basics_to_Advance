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
@app.callback(
    [Output('covid-graph', 'figure'), Output('live-text', 'children')],
    [Input('country-dropdown', 'value')]
)
def update_dashboard(country):
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=30"
    data = requests.get(url).json()

    if 'timeline' not in data:
        return {}, "No data available."

    timeline = data['timeline']
    dates = list(timeline['cases'].keys())

    cases = list(timeline['cases'].values())
    deaths = list(timeline['deaths'].values())
    recovered = list(timeline['recovered'].values())
    fig = {
        'data': [
            go.Scatter(x=dates, y=cases, name='Cases', line=dict(color='orange')),
            go.Scatter(x=dates, y=deaths, name='Deaths', line=dict(color='red')),
            go.Scatter(x=dates, y=recovered, name='Recovered', line=dict(color='green')),
        ],
        'layout': go.Layout(
            title=f"COVID-19 in {country} (Last 30 days)",
            xaxis={'title': 'Date'},
            yaxis={'title': 'Count'},
            hovermode='closest'
        )
    }
    latest = f"🦠 Latest Stats for {country} — Cases: {cases[-1]} | Deaths: {deaths[-1]} | Recovered: {recovered[-1]}"
    return fig, latest