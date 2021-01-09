import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly_express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_excel("https://github.com/chris1610/pbpython/blob/master/data/salesfunnel.xlsx?raw=True", engine="openpyxl")
mgr = df.Manager.unique()
orders_all = (df
            .groupby(['Name','Status'])
            .Quantity.sum()
            .reset_index()
            )
    
fig_all = px.bar(orders_all, 
        x='Name', 
        y='Quantity',
        color='Status',
        title='Order Status by Customer')

app.layout = html.Div([
    html.H2('This is my first plotly Dash'),
    dcc.Dropdown(id = 'manager-dropdown',
                options = [{'label': i, 'value' : i} for i in mgr],
                value=None),
    html.Div(id='selected-manager-div', children='selected manager is: '),
    dcc.Graph(id='sales-funnel-bar-graph', figure=fig_all)
])


### add interactiveness
@app.callback(Output(component_id='selected-manager-div',
                    component_property='children'),
             Input(component_id='manager-dropdown', 
                   component_property='value'))
def update_manager_selection(manager_dropdown_value):
    return 'selected manager is: {}'.format(manager_dropdown_value)


@app.callback(Output(component_id='sales-funnel-bar-graph',
                    component_property='figure'),
             Input(component_id='manager-dropdown',
                  component_property='value'))
def update_graph(manager_dropdown_value):
    
    if manager_dropdown_value is None:
        return fig_all
    else:
        df_plot = df.query('Manager == "{}"'.format(manager_dropdown_value))
        title = 'Sales funnel of {}'.format(manager_dropdown_value)
        
        orders = (df_plot
                .groupby(['Name','Status'])
                .Quantity.sum()
                .reset_index()
                )
            
        fig = px.bar(orders, 
            x='Name', 
            y='Quantity',
            color='Status',
            title=title)
        
        return fig

if __name__ == '__main__':
    app.run_server()