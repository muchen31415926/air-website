from dash import html, dcc, Patch
import plotly.express as px
import dash_bootstrap_components as dbc

from db_wrapper import DBWrapper


class GraphManager:
    def __init__(self):
        self.db = DBWrapper()
        self.fields = ['tvoc', 'eco2', 'pm25', 'pm10']

    def create_graphs(self, time_unit):  
        print(f'create_graphs({time_unit}): started')

        docs = self._get_db_docs(time_unit)
        print(f'create_graphs({time_unit}): got data from db')
        
        graphs = []   
        for field in self.fields:      
            fig = self._create_figure(docs, field) 
            self._set_figure_layout(fig, field, time_unit)   
            
            graph = dcc.Graph(id=f'{time_unit}-{field}-graph', figure=fig)
            graph_div = html.Div(className='graph', children=graph)

            if time_unit == "second":
                graphs.append(dbc.Col(graph_div, width=6))                                          
            else:
                graphs.append(graph_div)

        print(f'create_graphs({time_unit}): finished')
        return dbc.Row(graphs)

    def update_graphs(self, time_unit):
        print(f'update_graphs({time_unit}): started')

        docs = self._get_db_docs(time_unit)
        print(f'update_graphs({time_unit}): got data from db')

        patches = []  
        for field in self.fields:  
            patch = Patch()
            x, y = self._get_xy_data(docs, field)

            patch["data"][0]["x"] = x
            patch["data"][0]["y"] = y

            patches.append(patch)

        print(f'update_graphs({time_unit}): finished')
        return patches

    def _create_figure(self, docs, field):       
        x, y = self._get_xy_data(docs, field) 
        fig = px.line(x=x, y=y)                
        return fig

    def _set_figure_layout(self, fig, field, time_unit):
        common = {
            "paper_bgcolor": "#161b22",
            "plot_bgcolor": "#161b22",
            "font_color": "#e6edf3",

            "title": {
                "text": field.upper(),
                "font": {
                    "color": "#e6edf3"
                }
            },

            "xaxis": {
                "gridcolor": "#30363d",
                "zeroline": False
            },

            "yaxis": {
                "gridcolor": "#30363d",
                "zeroline": False
            }
        }
        
        if time_unit == "second":
            fig.update_layout(
                **common,
                height=300,                
                title_font_size=18
            )        
        elif time_unit == "minute":
            fig.update_layout(
                **common,
                margin_t = 100,               
                title_font_size=22,
                title_y=0.9
            )
            
    def _get_db_docs(self, time_unit):
        return self.db.find_data(time_unit)

    @staticmethod
    def _get_xy_data(docs, field):
        timestamps = [doc['timestamp'] for doc in docs]
        data = [doc[field] for doc in docs]

        return timestamps, data
