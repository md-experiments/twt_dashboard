import dash
import sys
#sys.path.append('/Users/md/Downloads/cc_f20')
__author__ = 'CountingChickens'

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

from pages.nav import card
from pages.news_data import select_nws



def stk_twt_layout(n, topic):
    links=['SPX','NASDAQ100','TSX','stoxx600','ASX','FTSE100']
    titles=['SPX','NASDAQ100','TSX','STOXX600','ASX','FTSE100']
    
    titles.pop(links.index(topic))
    links.remove(topic)
    n=select_nws(topic.upper())
    patterns = ['Sentiment ']*len(links)

    if len(n.df_tpc)==0:
        return html.Div([
                        html.H1(id='nws-h1',children=f'{topic} Social Sentiment 48hrs rolling'),
                        html.Div(id='page-2-content'),
                        html.Br(),
                        html.Div(card(links,titles, patterns), className='container-fluid'),
        ]
        )

    else:    
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
                go.Bar(x=list(n.df_tpc.index.values), y=list(n.df_tpc.Mentions.values), name='Nr Tweets (lhs)',alignmentgroup='b', base="stack"),
                secondary_y=False,
            )
        if 'Score_neg' in n.df_tpc.columns:
            neg_bar_vals = list(n.df_tpc.Score_neg.values)
            pos_bar_vals = list(n.df_tpc.Score.values)
        else:
            neg_bar_vals = list(n.df_tpc.Score.clip(-10,0).values)
            pos_bar_vals = list(n.df_tpc.Score.clip(0,10).values)

        fig.add_trace(
            go.Bar(x=list(n.df_tpc.index.values), y=neg_bar_vals, alignmentgroup='a', base="stack",showlegend=False, width=0.5),
            secondary_y=True,
        )
        fig.add_trace(
            go.Bar(x=list(n.df_tpc.index.values), y=pos_bar_vals, name="Sentiment",alignmentgroup='a', base="stack",showlegend=False, width=0.5),
            secondary_y=True,
        )

        fig.update_layout(
            barmode='stack',
            title_text=n.topic_title,
            showlegend=True,
            legend=dict(
                    x=0,
                    y=1.0
                ),
            yaxis=dict(title='Nr Tweets', side='left'),
            yaxis2=dict(title='Net Sentiment',
                        side='right', range=[-1, 1]),
            template='plotly_white',
            margin=dict(l=40, r=40, t=40, b=80)
        )

        return html.Div([
                        html.H1(id='nws-h1',children=f'{topic} Social Sentiment 48hrs rolling'),
                        html.Div(id='page-2-content'),
                        html.Br(),
                        html.Div(card(links,titles, patterns), className='container-fluid'),
                        html.Div(id='dash-container',
                            children=[
                                html.Div(
                                    [dcc.Graph(
                                    style={'height': 300},
                                    id='nws-bar-mentions-counts',
                                    figure=fig
                                    )]  ,
                                    #style={'width': '25%', 'display': 'inline-block'}
                                    ), 
                                dcc.Markdown(n.caveats), 
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
