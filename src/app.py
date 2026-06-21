from dash import Dash, html, callback, Output, Input, dcc

from charts import get_graphs, get_figures


app = Dash()
app.layout = [
    html.H1(children='Air Quality Monitor', style={'textAlign':'center'}),
    html.Div(id='graphs-container', children=get_graphs()),
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
    return get_figures()

if __name__ == '__main__':
    app.run(debug=True)
