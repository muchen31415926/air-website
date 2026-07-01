from dash import Dash, html, callback, Output, Input, dcc, Patch
import dash_bootstrap_components as dbc

from graph import GraphManager


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
graph_manager = GraphManager()

app.layout = [
    html.H1(children='Air Quality Monitor', style={'textAlign':'center'}),
    html.Div(children=graph_manager.create_graphs(time_unit="second")),
    html.Div(children=graph_manager.create_graphs(time_unit="minute")),
    dcc.Interval(id="second-update-interval", interval=3*1000),
    dcc.Interval(id="minute-update-interval", interval=6*10000)
]

@callback(
    Output('second-tvoc-graph', 'figure'),
    Output('second-eco2-graph', 'figure'),
    Output('second-pm25-graph', 'figure'),
    Output('second-pm10-graph', 'figure'),
    Input('second-update-interval', 'n_intervals')
)
def update_second_figures(_):
    return graph_manager.create_patches(time_unit="second")

@callback(
    Output('minute-tvoc-graph', 'figure'),
    Output('minute-eco2-graph', 'figure'),
    Output('minute-pm25-graph', 'figure'),
    Output('minute-pm10-graph', 'figure'),
    Input('minute-update-interval', 'n_intervals')
)
def update_minute_figures(_):
    return graph_manager.create_patches(time_unit="minute")

if __name__ == '__main__':
    app.run(debug=True)
