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
#from pages.twt_data import tw


def twt_layout(tw, topic):
    links=['AI','TEA','COFFEE']
    links.remove(topic)

    return html.Div([
    html.H1(id='twt-h1',children=f'#{topic} Tweets Dashboard'),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link(f'Go to #{links[0]}', href=f'/{links[0]}'),
    html.Br(),
    dcc.Link(f'Go to #{links[1]}', href=f'/{links[1]}'),
    html.Br(),   
    dcc.Link('Go to News', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    html.Div(id='dash-container',
                        children=[

                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='twt-bar-mentions-counts',
                                figure=dict(
                                    data= [
                                            {'x': list(tw.df_tpc.index.values), 'y': list(tw.df_tpc.Mentions.values), 'type': 'bar', 'name': tw.topic_label}
                                        ],
                                    layout=dict(
                                        title=tw.topic_title,
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
                                id='twt-graph'
                                )]  ,
                                style={'width': '70%', 'display': 'inline-block'}
                                ), 
                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='twt-bar-authors-counts',
                                )]  ,
                                style={'width': '30%', 'display': 'inline-block'}
                                ), 
                            html.H1('',''),
                            html.Div(
                                [dash_table.DataTable(
                                id='twt-table',
                                columns=[{"name": i, "id": i} for i in tw.cols_from_txt],
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
                            )]
                            )
                        ])
                    ])