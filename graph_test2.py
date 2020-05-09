import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go
import pandas as pd
#from colour import Color
from datetime import datetime
#from textwrap import dedent as d
import json

from pages.graph import build_graph
from pages.utils import FrameStacker


app = dash.Dash(__name__,)
#app.title = "Transaction Network"


df=pd.read_csv('./data/macro_graph.csv',index_col=0).fillna('')

key_words=['Coronavirus']

relevant_kgs=list(df[df.ent_graph.apply(lambda x: len(set(key_words)& set(eval(x)))>0)].graph.values)

fs=FrameStacker()

'''
random_layout
shell_layout
spring_layout
spectral_layout
'''
if len(relevant_kgs)>0:
    for kg in relevant_kgs:
        k=pd.read_json(kg)
        fs.append(k)
    kg_df=fs.stack()
else:
    txt_kg='{"source":{"0":"Nothing"},"edge":{"0":"to"},"target":{"0":"show ..."}}'
    kg_df=pd.read_json(txt_kg)

#txt_kg='{"source":{"0":"Rolls-Royce ","1":"board"},"edge":{"0":"says","1":"leaves"},"target":{"0":"board","1":"Valueact executive "}}'
#kg_df=pd.read_json(txt_kg)

#fig.show()
app.layout = html.Div([
        dcc.Graph(
            figure=build_graph(kg_df,nx.shell_layout)
        )
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True)