from dash import Dash, html, callback, Output, Input, dcc
import dash_bootstrap_components as dbc

from graph import GraphManager
from sensor import SensorManager

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
graph_manager = GraphManager()
sensor_manager = SensorManager()

app.layout = [
    html.H5(id='sensor-status', children='Sensor： 線上🟢', style={'textAlign':'left'}),
    html.Div(children=graph_manager.create_graphs(time_unit="second")),
    html.Div(children=graph_manager.create_graphs(time_unit="minute")),
    dcc.Interval(id="second-update-interval", interval=3*1000),
    dcc.Interval(id="minute-update-interval", interval=6*10000),
    dcc.Interval(id="sensor-status-update-interval", interval=5*1000)
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

@callback(
    Output('sensor-status', 'children'),
    Input('sensor-status-update-interval', 'n_intervals')
)
def update_sensor_Status(_):
    if sensor_manager.is_online():
        return 'Sensor：🟢Online'
    
    return 'Sensor：🔴Offline'

if __name__ == '__main__':
    app.run(debug=True)
