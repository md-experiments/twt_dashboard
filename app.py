import dash
from pages import index, news, twt, stk_twt


import sys
#sys.path.append('/Users/md/Downloads/cc_f20')
__author__ = 'CountingChickens'

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.express as px

from flask import Flask, render_template, request, session, make_response

import pandas as pd
from pages.news_data import select_nws
from pages.twt_data import ai,cof,tea, fert, food, mind, select_tw
from pages.index import index_page
# You know, for Graph
import networkx as nx
from pages.graph import build_graph
from pages.utils import FrameStacker

import dash_bootstrap_components as dbc
from pages.nav import navbar

print(dcc.__version__) # 0.6.0 or above is required

#app = dash.Dash()
app = Flask(__name__)  # '__main__'

max_rows_table=100

import os 
#dir_path = os.path.dirname(os.path.realpath(__file__))
#os.chdir(dir_path)


'''@app.route("/", methods=["GET"])
def home():
    return app_dash.layout'''

external_stylesheets = [dbc.themes.LITERA]
'''[   dict(
        rel="stylesheet",
        href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" ,
        integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" ,
        crossorigin="anonymous"
    )
]'''

app_dash = Dash(__name__,
               server=app,
               url_base_pathname='/',
               external_stylesheets=external_stylesheets)

app_dash.config.suppress_callback_exceptions = True

app_dash.layout = html.Div([
    #html.Link(rel="icon", href=os.path.join(os.getcwd(), "/assets/logo.png")),
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content')
])
app_dash.title = 'CountingChickens'

'''@app.route("/dash")
def MyDashApp():
    app_dash.title = "Title: %s"%(path)
    return app_dash.index()
'''

# add callback for toggling the collapse on small screens
@app_dash.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Index Page callback
@app_dash.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboards/TEA':
        #app_dash.update_title = '#TEA | CountingChickens'
        return twt.twt_layout(tea,'TEA')
    elif pathname == '/dashboards/COFFEE':
        #app_dash.title = '#COFFEE | CountingChickens'
        return twt.twt_layout(cof,'COFFEE')
    elif pathname == '/dashboards/FERTILITY':
        #app_dash.title = '#FERTILITY | CountingChickens'
        return twt.twt_layout(fert,'FERTILITY')
    elif pathname == '/dashboards/MINDSET':
        #app_dash.title = '#MINDSET | CountingChickens'
        return twt.twt_layout(mind,'MINDSET')
    elif pathname == '/dashboards/FOOD':
        #app_dash.title = '#FOOD | CountingChickens'
        return twt.twt_layout(food,'FOOD')
    elif pathname == '/dashboards/AI':
        #app_dash.title = '#AI | CountingChickens'
        return twt.twt_layout(ai,'AI')
    elif pathname == '/dashboards/MACRO':
        #app_dash.title = 'Macro News | CountingChickens'
        return news.news_layout('','MACRO')
    elif pathname == '/dashboards/COMPANY':
        #app_dash.title = 'Company News | CountingChickens'
        return news.news_layout('','COMPANY')
    elif pathname == '/dashboards/SPX':
        #app_dash.title = 'Company News | CountingChickens'
        return stk_twt.stk_twt_layout('','SPX')
    elif pathname == '/dashboards/NASDAQ100':
        #app_dash.title = 'Company News | CountingChickens'
        return stk_twt.stk_twt_layout('','NASDAQ100')
    elif pathname == '/dashboards/TSX':
        #app_dash.title = 'Company News | CountingChickens'
        return stk_twt.stk_twt_layout('','TSX')
    elif pathname == '/dashboards/STOXX600':
        #app_dash.title = 'Company News | CountingChickens'
        return stk_twt.stk_twt_layout('','stoxx600')
    elif pathname == '/dashboards/ASX':
        #app_dash.title = 'Company News | CountingChickens'
        return stk_twt.stk_twt_layout('','ASX')
    elif pathname == '/dashboards/IBOV':
        #app_dash.title = 'Company News | CountingChickens'
        return stk_twt.stk_twt_layout('','IBOV')
    else:
        #app_dash.title = 'Nest page | CountingChickens'
        return index_page(os.getcwd())
        '''index.index_page'''
'''
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
'''

@app_dash.callback(Output('nws-graph',  'figure'),
              [Input('nws-bar-mentions-counts', 'clickData'),Input('nws-h1', 'children')])
def update_figure(list_from_click,title):
    '''
    if isinstance(list_of_stocks,str):
        list_of_stocks=[list_of_stocks]
    
    if list_from_click:
    '''
    n=select_nws(title)
    
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
              [Input('nws-bar-mentions-counts', 'clickData'),Input('nws-h1', 'children')])
def update_bar_authors(list_from_click, title):
    n=select_nws(title)

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


@app_dash.callback(Output('nws-table',  'children'),
              [Input('nws-bar-mentions-counts', 'clickData'),Input('nws-h1', 'children')])
def update_table(list_from_click,title):
    n=select_nws(title)

    if list_from_click:
        list_of_stocks=[clk['x'].lower() for clk in list_from_click['points']]
    else:
        list_of_stocks=[n.default_category]

    df_out=n.df_txt.copy()
    indicator=n.df_txt['Hashtags_lower'].apply(lambda x: len(set(x) & set(list_of_stocks))>0).values
    df_out=df_out[indicator].sort_values(n.sort_col, ascending=n.sort_ascending)
    df_out=df_out[n.cols_from_txt]
    
    df_out['#']=list(range(1,len(df_out)+1))
    new_cols=list(df_out.columns)
    new_cols.remove('#')
    df_out=df_out[['#']+new_cols]
    df_out=df_out.head(max_rows_table)
    return dbc.Table.from_dataframe(df_out,striped=True, bordered=True, hover=True)


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


'''@app_dash.callback(Output('twt-table',  'data'),'''
@app_dash.callback(Output('twt-table',  'children'),
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
    
    '''return df_out.to_dict('records')'''
    df_out['#']=list(range(1,len(df_out)+1))
    new_cols=list(df_out.columns)
    new_cols.remove('#')
    df_out=df_out[['#']+new_cols]
    df_out=df_out.head(max_rows_table)
    return dbc.Table.from_dataframe(df_out,striped=True, bordered=True, hover=True, responsive=True)


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


@app_dash.callback(Output('nws-map', 'figure'),
              [Input('nws-bar-mentions-counts', 'clickData'),Input('nws-h1', 'children')])
def update_map(list_from_click, title):
    ns=select_nws(title)

    if list_from_click:
        list_of_stocks=[clk['x'].lower() for clk in list_from_click['points']]
    else:
        list_of_stocks=[ns.default_category]

    selected_df=ns.df_geo[ns.df_geo.Term.isin(list_of_stocks)]

    rng_min=selected_df.Mentions.min()
    rng_max=selected_df.Mentions.max()
    figure=px.density_mapbox(data_frame=selected_df,lat='lat', lon='lon', z='Mentions', radius=20,
                            center = {"lat": 37.0902, "lon": -0.7129},zoom=0,
                            hover_name="location", hover_data=["Mentions", "Term"],
                            color_continuous_scale="Viridis",
                            range_color=(rng_min, rng_max),
                            mapbox_style="carto-positron")
    #figure.update_layout(margin={"r":1,"t":1.5,"l":1,"b":0.5})
    figure.update_layout(margin={"t":3,"b":6})
    return figure

@app_dash.callback(Output('nws-kg', 'figure'),
              [Input('nws-bar-mentions-counts', 'clickData'),Input('nws-h1', 'children')])
def update_kg(list_from_click, title):
    ns=select_nws(title)

    if list_from_click:
        list_of_stocks=[clk['x'].lower() for clk in list_from_click['points']]
    else:
        list_of_stocks=[ns.default_category]

    df_out=ns.df_grph.copy()
    indicator=ns.df_grph['Hashtags_lower'].apply(lambda x: len(set(x) & set(list_of_stocks))>0).values
    relevant_kgs=list(df_out[indicator].graph.values)
    
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

    figure=build_graph(kg_df,nx.spring_layout)

    return figure
#if __name__ == '__main__':
#    app.run_server(host='0.0.0.0',debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
