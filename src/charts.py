from dash import html, dcc
import plotly.express as px

from db_wrapper import DBWrapper


fields = ['tvoc', 'eco2', 'pm25', 'pm10']

db = DBWrapper()

def get_graphs():
    graphs = []
    for field in fields:      
        graph = dcc.Graph(id=f'{field}-graph', figure={})
        graph_div = html.Div(className='graph', children=graph)

        graphs.append(graph_div)

    return graphs

def get_figures():
    docs = db.find_data()
    print('successfully get data from db')

    figs = []
    timestamps = [doc['timestamp'] for doc in docs]    
    for field in fields:  
        data = [doc[field] for doc in docs]      
        fig = px.line(x=timestamps, y=data, title=field.upper())
        figs.append(fig)

    return figs