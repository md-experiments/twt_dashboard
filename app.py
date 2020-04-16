import dash
from pages import index, news, twt


import sys
#sys.path.append('/Users/md/Downloads/cc_f20')
__author__ = 'CountingChickens'

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

from flask import Flask, render_template, request, session, make_response

import pandas as pd
from pages.news_data import n
from pages.twt_data import ai,cof,tea

tw=tea

print(dcc.__version__) # 0.6.0 or above is required

#app = dash.Dash()
app = Flask(__name__)  # '__main__'
app_dash = Dash(__name__,
               server=app,
               url_base_pathname='/')

app_dash.config.suppress_callback_exceptions = True

app_dash.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Page 1 callback
@app_dash.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)

# Page 2
@app_dash.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

# Index Page callback
@app_dash.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/TEA':
        return twt.twt_layout(tea,'TEA')
    if pathname == '/COFFEE':
        return twt.twt_layout(cof,'COFFEE')
    if pathname == '/AI':
        return twt.twt_layout(ai,'AI')


    elif pathname == '/page-2':
        return news.page_2_layout
    else:
        return index.index_page
'''
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
'''

@app_dash.callback(Output('nws-graph',  'figure'),
              [Input('nws-bar-mentions-counts', 'clickData')])
def update_figure(list_from_click):
    '''
    if isinstance(list_of_stocks,str):
        list_of_stocks=[list_of_stocks]
    
    if list_from_click:
    '''
    
    if list_from_click:
        list_of_topics=[clk['x'] for clk in list_from_click['points']]
    else:
        list_of_topics=[n.default_category]

    data=[
            dict(
                    x=list(n.df_tim[n.df_tim.term==hashtag.lower()].time.values),
                    y=list(n.df_tim[n.df_tim.term==hashtag.lower()].id.values),
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

@app_dash.callback(Output('nws-bar-authors-counts',  'figure'),
              [Input('nws-bar-mentions-counts', 'clickData')])
def update_bar_authors(list_from_click):

    if list_from_click:
        list_of_topics=[clk['x'] for clk in list_from_click['points']]
    else:
        list_of_topics=[n.default_category]
    
    data=[
            dict(
                    x=list(n.df_aut[n.df_aut.term==hashtag.lower()][n.col_entity].iloc[:n.authors_limit].values),
                    y=list(n.df_aut[n.df_aut.term==hashtag.lower()].id.iloc[:n.authors_limit].values),
                    type='bar',
                    name='#'+hashtag,
                ) for hashtag in list_of_topics
        ]
    return dict(
        data= data,
        layout=dict(
            title=n.authors_title,
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=80)
        )
        )


@app_dash.callback(Output('nws-table',  'data'),
              [Input('nws-bar-mentions-counts', 'clickData')])
def update_table(list_from_click):

    if list_from_click:
        list_of_stocks=[clk['x'].lower() for clk in list_from_click['points']]
    else:
        list_of_stocks=[n.default_category]

    df_out=n.df_txt.copy()
    indicator=n.df_txt['Hashtags_lower'].apply(lambda x: len(set(x) & set(list_of_stocks))>0).values
    df_out=df_out[indicator].sort_values(n.sort_col, ascending=n.sort_ascending)
    df_out=df_out[n.cols_from_txt]
    
    return df_out.to_dict('records')


@app_dash.callback(Output('twt-graph',  'figure'),
              [Input('twt-bar-mentions-counts', 'clickData'),Input('twt-h1', 'children')])
def update_figure(list_from_click, title):
    if title.startswith('#TEA'):
        tw=tea
    elif title.startswith('#COFFEE'):
        tw=cof
    else:
        tw=ai

    if list_from_click:
        list_of_topics=[clk['x'] for clk in list_from_click['points']]
    else:
        list_of_topics=[tw.default_category]

    data=[
            dict(
                    x=list(tw.df_tim[tw.df_tim.term==hashtag.lower()].time.values),
                    y=list(tw.df_tim[tw.df_tim.term==hashtag.lower()].id.values),
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

@app_dash.callback(Output('twt-bar-authors-counts',  'figure'),
              [Input('twt-bar-mentions-counts', 'clickData'),Input('twt-h1', 'children')])
def update_bar_authors(list_from_click, title):
    if title.startswith('#TEA'):
        tw=tea
    elif title.startswith('#COFFEE'):
        tw=cof
    else:
        tw=ai

    if list_from_click:
        list_of_topics=[clk['x'] for clk in list_from_click['points']]
    else:
        list_of_topics=[tw.default_category]

    data=[
            dict(
                    x=list(tw.df_aut[tw.df_aut.term==hashtag.lower()].original_user.iloc[:tw.authors_limit].values),
                    y=list(tw.df_aut[tw.df_aut.term==hashtag.lower()].id.iloc[:tw.authors_limit].values),
                    type='bar',
                    name='#'+hashtag,
                ) for hashtag in list_of_topics
        ]
    return dict(
        data= data,
        layout=dict(
            title=tw.authors_title,
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=80)
        )
        )


@app_dash.callback(Output('twt-table',  'data'),
              [Input('twt-bar-mentions-counts', 'clickData'),Input('twt-h1', 'children')])
def update_table(list_from_click, title):
    if title.startswith('#TEA'):
        tw=tea
    elif title.startswith('#COFFEE'):
        tw=cof
    else:
        tw=ai

    if list_from_click:
        list_of_stocks=[clk['x'].lower() for clk in list_from_click['points']]
    else:
        list_of_stocks=[tw.default_category]

    df_out=tw.df_txt.copy()
    indicator=tw.df_txt['Hashtags_lower'].apply(lambda x: len(set(x) & set(list_of_stocks))>0).values
    df_out=df_out[indicator].sort_values(tw.txt_sort_col, ascending=tw.txt_sort_ascending)
    df_out=df_out[tw.cols_from_txt]
    
    return df_out.to_dict('records')


#if __name__ == '__main__':
#    app.run_server(host='0.0.0.0',debug=True)


@app.route("/dash")
def MyDashApp():
    return app_dash.index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
