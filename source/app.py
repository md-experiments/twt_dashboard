import sys
#sys.path.append('/Users/md/Downloads/cc_f20')


__author__ = 'CountingChickens'

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import pandas as pd

from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)  # '__main__'


app_dash = Dash(__name__,
               server=app,
               url_base_pathname='/')

df_tpc=pd.read_csv('AI_topics.csv', index_col=0)
selected_topics=[tpc.lower() for tpc in df_tpc.index.values]

df_aut=pd.read_csv('AI_authors.csv', index_col=0)
df_tim=pd.read_csv('AI_time.csv', index_col=0)
df_txt=pd.read_csv('AI_body.csv', index_col=0)
df_txt=df_txt.rename(columns={'Favorite Count': 'Favs','Retweet Count': 'RT'})
cols_from_txt=list(df_txt.columns.values)
cols_from_txt.remove('Place')
cols_from_txt.remove('Id Str')
df_txt['Hashtags_lower']=df_txt.Hashtags.apply(lambda x: [z.lower() for z in eval(x)])
df_txt['Hashtags']=df_txt.Hashtags.apply(lambda x: ', '.join(["#" + z for z in eval(x)]))
df_txt['Url']=df_txt.Url.apply(lambda x: ', '.join([z for z in eval(x)]))
df_txt['Mentions']=df_txt.Mentions.apply(lambda x: ', '.join(["@" + z for z in eval(x)]))

app_dash.layout = html.Div(id='dash-container',
                        children=[

                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='bar-mentions-counts',
                                figure=dict(
                                    data= [
                                            {'x': list(df_tpc.index.values), 'y': list(df_tpc.Mentions.values), 'type': 'bar', 'name': 'Nr Tweets'}
                                        ],
                                    layout=dict(
                                        title='Top 50 Hashtags for #AI',
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
                                id='my-graph'
                                )]  ,
                                style={'width': '70%', 'display': 'inline-block'}
                                ), 
                            html.Div(
                                [dcc.Graph(
                                style={'height': 300},
                                id='bar-authors-counts',
                                )]  ,
                                style={'width': '30%', 'display': 'inline-block'}
                                ), 
                            html.H1('',''),
                            html.Div(
                                [dash_table.DataTable(
                                id='nws-table',
                                columns=[{"name": i, "id": i} for i in cols_from_txt],
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

@app_dash.callback(Output('my-graph',  'figure'),
              [Input('bar-mentions-counts', 'clickData')])
def update_figure(list_from_click):
    '''
    if isinstance(list_of_stocks,str):
        list_of_stocks=[list_of_stocks]
    
    if list_from_click:
    '''
    
    if list_from_click:
        list_of_topics=[clk['x'] for clk in list_from_click['points']]
    else:
        list_of_topics=['ai']

    data=[
            dict(
                    x=list(df_tim[df_tim.term==hashtag.lower()].time.values),
                    y=list(df_tim[df_tim.term==hashtag.lower()].id.values),
                    name=hashtag,
                ) for hashtag in list_of_topics
        ]
    return dict(
        data=data
        ,
        layout=dict(
            title='Mentions over time',
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            xaxis=dict(type='category',nticks=15),
            xaxis_tickformat ='%Y-%m-%d',            
            margin=dict(l=40, r=0, t=40, b=70), 
        )
    )

@app_dash.callback(Output('bar-authors-counts',  'figure'),
              [Input('bar-mentions-counts', 'clickData')])
def update_bar_authors(list_from_click):

    if list_from_click:
        list_of_topics=[clk['x'] for clk in list_from_click['points']]
    else:
        list_of_topics=['ai']
    authors_limit=30
    data=[
            dict(
                    x=list(df_aut[df_aut.term==hashtag.lower()].original_user.iloc[:authors_limit].values),
                    y=list(df_aut[df_aut.term==hashtag.lower()].id.iloc[:authors_limit].values),
                    type='bar',
                    name='#'+hashtag,
                ) for hashtag in list_of_topics
        ]
    return dict(
        data= data,
        layout=dict(
            title='Nr Tweets by Author per Hashatag',
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=80)
        )
        )


@app_dash.callback(Output('nws-table',  'data'),
              [Input('bar-mentions-counts', 'clickData')])
def update_table(list_from_click):

    if list_from_click:
        list_of_stocks=[clk['x'].lower() for clk in list_from_click['points']]
    else:
        list_of_stocks=['ai']

    df_out=df_txt.copy()
    indicator=df_txt['Hashtags_lower'].apply(lambda x: len(set(x) & set(list_of_stocks))>0).values
    df_out=df_out[indicator].sort_values('Favs', ascending=False)
    df_out=df_out[cols_from_txt]
    
    return df_out.to_dict('records')


@app.route("/dash")
def MyDashApp():
    return app_dash.index()

if __name__ == '__main__':
    app.run(port=4990, debug=True)
