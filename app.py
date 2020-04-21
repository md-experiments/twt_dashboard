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
import plotly.express as px

from flask import Flask, render_template, request, session, make_response

import pandas as pd
from pages.news_data import n
from pages.twt_data import ai,cof,tea, fert, food, mind, select_tw

print(dcc.__version__) # 0.6.0 or above is required

#app = dash.Dash()
app = Flask(__name__)  # '__main__'


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

external_stylesheets = [
    dict(
        rel="stylesheet",
        href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" ,
        integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" ,
        crossorigin="anonymous"
    )
]

app_dash = Dash(__name__,
               server=app,
               url_base_pathname='/dashboards/',
               external_stylesheets=external_stylesheets)

app_dash.config.suppress_callback_exceptions = True

app_dash.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])
app_dash.title = 'CountingChickens'

'''@app.route("/dash")
def MyDashApp():
    app_dash.title = "Title: %s"%(path)
    return app_dash.index()
'''
# Index Page callback
@app_dash.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboards/TEA':
        app_dash.update_title = '#TEA | CountingChickens'
        return twt.twt_layout(tea,'TEA')
    elif pathname == '/dashboards/COFFEE':
        app_dash.title = '#COFFEE | CountingChickens'
        return twt.twt_layout(cof,'COFFEE')
    elif pathname == '/dashboards/FERTILITY':
        app_dash.title = '#FERTILITY | CountingChickens'
        return twt.twt_layout(fert,'FERTILITY')
    elif pathname == '/dashboards/MINDSET':
        app_dash.title = '#MINDSET | CountingChickens'
        return twt.twt_layout(mind,'MINDSET')
    elif pathname == '/dashboards/FOOD':
        app_dash.title = '#FOOD | CountingChickens'
        return twt.twt_layout(food,'FOOD')
    elif pathname == '/dashboards/AI':
        app_dash.title = '#AI | CountingChickens'
        return twt.twt_layout(ai,'AI')
    elif pathname == '/dashboards/NEWS':
        app_dash.title = 'News | CountingChickens'
        return news.page_2_layout
    else:
        app_dash.title = 'Nest page | CountingChickens'
        return render_template("home.html")
        '''index.index_page'''
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
    tw=select_tw(title)

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
    tw=select_tw(title)

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
    tw=select_tw(title)

    if list_from_click:
        list_of_stocks=[clk['x'].lower() for clk in list_from_click['points']]
    else:
        list_of_stocks=[tw.default_category]

    df_out=tw.df_txt.copy()
    indicator=tw.df_txt['Hashtags_lower'].apply(lambda x: len(set(x) & set(list_of_stocks))>0).values
    df_out=df_out[indicator].sort_values(tw.txt_sort_col, ascending=tw.txt_sort_ascending)
    df_out=df_out[tw.cols_from_txt]
    
    return df_out.to_dict('records')


@app_dash.callback(Output('twt-map',  'figure'),
              [Input('twt-bar-mentions-counts', 'clickData'),Input('twt-h1', 'children')])
def update_map(list_from_click, title):
    tw=select_tw(title)

    if list_from_click:
        list_of_stocks=[clk['x'].lower() for clk in list_from_click['points']]
    else:
        list_of_stocks=[tw.default_category]

    selected_df=tw.df_geo[tw.df_geo.Term.isin(list_of_stocks)]

    rng_min=selected_df.Tweets.min()
    rng_max=selected_df.Tweets.max()
    figure=px.density_mapbox(data_frame=selected_df,lat='lat', lon='lon', z='Tweets', radius=20,
                            center = {"lat": 37.0902, "lon": -0.7129},zoom=0,
                            hover_name="original_location", hover_data=["Tweets", "Term"],
                            color_continuous_scale="Viridis",
                            range_color=(rng_min, rng_max),
                            mapbox_style="carto-positron")
    #figure.update_layout(margin={"r":1,"t":1.5,"l":1,"b":0.5})
    figure.update_layout(margin={"t":3,"b":6})
    return figure

#if __name__ == '__main__':
#    app.run_server(host='0.0.0.0',debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
