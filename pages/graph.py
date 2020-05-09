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


def build_graph(kg_df,nx_layout):

    #text_ls
    G=nx.from_pandas_edgelist(kg_df, "source", "target", 
                                edge_attr=True, create_using=nx.MultiDiGraph())
    pos=nx_layout(G)
    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_text=list(kg_df.edge.values)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines',
        #text=['Assss','Bsss'],
        #textposition="top center",
        #hovertext=['ss','ddd']
        )

    node_x = []
    node_y = []
    #text=[]

    index=0
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
        #text.append()
        index+=1

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text', textposition="bottom center",
        hoverinfo='text',
        text=[str(node).strip() for node in G.nodes],
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Blues',
            reversescale=True,
            color=[],
            size=30,
            #colorbar=dict(
            #    thickness=15,
            #    title='Node Connections',
            #    xanchor='left',
            #    titleside='right'
            #),
            line_width=1)
            )

    return go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Graph of relations to main entity',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[
                                dict(
                                    ax=(G.nodes[edge[0]]['pos'][0] + G.nodes[edge[1]]['pos'][0]) / 2,
                                    ay=(G.nodes[edge[0]]['pos'][1] + G.nodes[edge[1]]['pos'][1]) / 2, axref='x', ayref='y',
                                    x=(G.nodes[edge[1]]['pos'][0] * 3 + G.nodes[edge[0]]['pos'][0]) / 4,
                                    y=(G.nodes[edge[1]]['pos'][1] * 3 + G.nodes[edge[0]]['pos'][1]) / 4, xref='x', yref='y',
                                    text=edge_text[ii],
                                    height=50,
                                    font=dict(size=18),
                                    #textangle=45,
                                    showarrow=True,
                                    arrowhead=3,
                                    arrowsize=4,
                                    arrowwidth=1,
                                    opacity=1
                                ) for (ii,edge) in enumerate(G.edges)
                                ],
                    #xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    #yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                        )
                    )

