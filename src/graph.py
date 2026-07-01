from dash import html, dcc, Patch
import plotly.express as px
import dash_bootstrap_components as dbc

from db_wrapper import DBWrapper


class GraphManager:
    def __init__(self):
        self.db = DBWrapper()
        self.fields = ['tvoc', 'eco2', 'pm25', 'pm10']

    def create_graphs(self, time_unit):    
        docs = self._get_db_docs(time_unit)
        
        graphs = []   
        for field in self.fields:      
            fig = self._create_figure(docs, field, time_unit)    
            
            graph = dcc.Graph(id=f'{time_unit}-{field}-graph', figure=fig)
            graph_div = html.Div(className='graph', children=graph)

            if time_unit == "second":
                graphs.append(dbc.Col(graph_div, width=6))                          
            else:
                graphs.append(graph_div)
        
        return dbc.Row(graphs)

    def create_patches(self, time_unit):
        docs = self._get_db_docs(time_unit)

        patches = []  
        for field in self.fields:  
            patch = Patch()
            x, y = self._get_xy_data(docs, field)

            patch["data"][0]["x"] = x
            patch["data"][0]["y"] = y

            patches.append(patch)
        return patches

    def _create_figure(self, docs, field, time_unit):       
        x, y = self._get_xy_data(docs, field) 
        fig = px.line(x=x, y=y)      
          
        fig.update_layout(
            paper_bgcolor='#0d1117',
            plot_bgcolor='#161b22',
            margin_t = 100,
            font_color = '#e6edf3',
            
            title=dict(
                text=field.upper(),
                font=dict(
                    size=22,
                    color='#e6edf3'
                ),
                y=0.9,
            ),

            xaxis=dict(
                rangeslider=dict(visible=True),
                gridcolor='#30363d',
                zeroline=False
            ),

            yaxis=dict(
                gridcolor='#30363d',
                zeroline=False
            )
    )
        
        return fig

    def _get_db_docs(self, time_unit):
        return self.db.find_data(time_unit)

    @staticmethod
    def _get_xy_data(docs, field):
        timestamps = [doc['timestamp'] for doc in docs]
        data = [doc[field] for doc in docs]

        return timestamps, data
