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



def stk_twt_layout(n, topic):
    links=['SPX','NASDAQ100','TSX','stoxx600','ASX','IBOV']
    titles=['SPX','NASDAQ100','TSX','STOXX600','ASX','IBOV']
    pattern = 'Sentiment '
    titles.pop(links.index(topic))
    links.remove(topic)
    n=select_nws(topic.upper())
    return html.Div([
                    html.H1(id='nws-h1',children=f'{topic} Social Sentiment 48hrs rolling'),
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
                                            {'x': list(n.df_tpc.index.values), 'y': list(n.df_tpc.Mentions.values), 'type': 'bar', 'name': 'Nr Tweets'},
                                            {'x': list(n.df_tpc.index.values), 'y': list(n.df_tpc.Score.values), 'type': 'bar', 'name': 'Net Sentiment'}
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
                            html.Div(
                                id='nws-table',
                            )
                        ]),
])
