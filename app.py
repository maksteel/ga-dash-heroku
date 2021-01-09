import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly_express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_excel("https://github.com/chris1610/pbpython/blob/master/data/salesfunnel.xlsx?raw=True")
mgr = df.Manager.unique()


app.layout = html.Div([
    html.H2('This is my first plotly Dash'),
    dcc.Dropdown(id = 'manager-dropdown',
                options = [{'label': i, 'value' : i} for i in mgr],
                value=None),
    html.Div(id='selected-manager-div', children='selected manager is: '),
    dcc.Graph(id='sales-funnel-bar-graph', figure=None)
])

if __name__ == '__main__':
    app.run_server()