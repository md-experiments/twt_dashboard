import dash
import sys
#sys.path.append('/Users/md/Downloads/cc_f20')
__author__ = 'CountingChickens'

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import pandas as pd

from pages.nav import card
from pages.news_data import select_nws



def news_layout(n, topic):
    links=['MACRO','COMPANY']
    titles=['Macro','Company']
    pattern = 'News '
    titles.pop(links.index(topic))
    links.remove(topic)
    n=select_nws(topic.upper())
    return html.Div([
                    html.H1(id='nws-h1',children=f'{topic} News Dashboard February 2020'),
                    html.Div(id='page-2-content'),
                    html.Br(),
                    html.Div(card(links,titles, pattern), className='container-fluid'),
                    html.Div(id='dash-container',
                        children=[
                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='nws-bar-mentions-counts',
                                figure=dict(
                                    data= [
                                            {'x': list(n.df_tpc.index.values), 'y': list(n.df_tpc.Mentions.values), 'type': 'bar', 'name': 'Nr Tweets'}
                                        ],
                                    layout=dict(
                                        title=n.topic_title,
                                        showlegend=True,
                                        legend=dict(
                                            x=0,
                                            y=1.0
                                        ),
                                        margin=dict(l=40, r=0, t=40, b=80)
                                    )
                                )
                                )]  ,
                                #style={'width': '25%', 'display': 'inline-block'}
                                ), 
                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='nws-graph'
                                )]  ,
                                style={'width': '30%', 'display': 'inline-block'}
                                ), 
                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='nws-map'
                                )]  ,
                                style={'width': '40%', 'display': 'inline-block'}
                                ), 
                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='nws-bar-authors-counts',
                                )]  ,
                                style={'width': '30%', 'display': 'inline-block'}
                                ), 
                            html.H1('',''),
                            html.Div([
                                    dcc.Graph(
                                        id='nws-kg',
                                    )
                                ]
                            ),
                            html.H1('',''),
                            html.Div(
                                id='nws-table',
                            )
                        ]),
])


'''[dash_table.DataTable(
                                id='nws-table',
                                columns=[{"name": i, "id": i} for i in n.cols_from_txt],
                                #fixed_rows={'headers': True},
                                style_cell={'textAlign': 'left'},
                                style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto'
                                    },
                                style_as_list_view=True,
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                                style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'
                                }
                            )]'''