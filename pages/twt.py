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

def card(nr,link_nm,title):
    return html.Div(
        id=f'main-{nr}',
        children=[
            html.Br(),
            html.Img(src=f'/static/{link_nm}.png', className='card-img'),
            dcc.Link(f'Twitter: #{title}', href=f'/dashboards/{link_nm.upper()}'),
            ],
        style={'width': '15%', 'display': 'inline-block'},
        className='card'  
    )


def twt_layout(tw, topic):
    links=['TEA','COFFEE','FOOD','FERTILITY','MINDSET','AI']
    titles=['Tea','Coffee','Food','Fertility','LifeCoach','AI']
    titles.pop(links.index(topic))
    links.remove(topic)
    

    return html.Div([
    html.H1(id='twt-h1',children=f'#{topic} Tweets Dashboard'),
    html.Div(id='page-1-content'),
    html.Div([card(i,links[i],titles[i]) for i in range(len(links))]),
    html.Br(),   
    dcc.Link('Go to News', href='/NEWS'),
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
                                style={'width': '30%', 'display': 'inline-block'}
                                ), 
                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='twt-map'
                                )]  ,
                                style={'width': '40%', 'display': 'inline-block'}
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
                                style_table={'width': '1'},
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