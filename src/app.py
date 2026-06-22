from dash import Dash, html, callback, Output, Input, dcc, Patch

from graph import GraphManager


app = Dash()
graph_manager = GraphManager()

app.layout = [
    html.H1(children='Air Quality Monitor', style={'textAlign':'center'}),
    html.Div(id='graphs-container', children=graph_manager.create_graphs()),
    dcc.Interval(id="update-interval", interval=3*1000)
]

@callback(
    Output('tvoc-graph', 'figure'),
    Output('eco2-graph', 'figure'),
    Output('pm25-graph', 'figure'),
    Output('pm10-graph', 'figure'),
    Input('update-interval', 'n_intervals')
)
def update_figures(_):
    return graph_manager.create_patches()

if __name__ == '__main__':
    app.run(debug=True)
