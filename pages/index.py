import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import os

links_twt=['TEA','COFFEE','FOOD','FERTILITY','MINDSET','AI']
titles_twt=['Tea','Coffee','Food','Fertility','LifeCoach','AI']
heads_twt=[
'Tea','Coffee','Food',
'Fertility','LifeCoach','AI']
pars_twt=[
    'Tweets for the Tea Nomad',    'Strong, black & bitter',    'Fabulous Fragrant Food',
    'Tweets about the blue line',    '#YouCanDoIt!',    'Fake brains, real tweets',
]
cols_twt=[
"text-white","text-white","text-white",
"text-white","text-dark","text-white"]

'''================= NEWS ===================='''
links_nws=['MACRO','COMPANY']
titles_nws=['Macro','Company']

heads_nws=['Macro News','Company News']

pars_nws=['Top trends in the news', 'Corporates in the news', ]

cols_nws=["text-white","text-white",]
import datetime
import json

def title_card(links,titles, heads, pars, cols,size="30rem", pattern='Twitter: #'):
    #with open(str(datetime.datetime.now()),'w') as f:
    #    json.dump(os.getcwd(),f)
    output=html.Div(
        dbc.Row([dbc.Col(dbc.Card(
            id=f'main-{i}',
            children=[
                #dbc.CardImg(src=f'/static/{links[i]}.png'),
                html.Img(src=os.path.join(os.getcwd(), f'/assets/{links[i].lower()}.png'), style={'width':'100%'}),
                dbc.CardBody(
                    [html.H3(heads[i], className=cols[i]),
                    html.P(pars[i], className=cols[i]),
                    dbc.Button(f'{pattern}{titles[i]}', href=f'/dashboards/{links[i].upper()}', size="sm", external_link=True),],
                    className='card-img-overlay'
                    )
                ],
            style={"width": size},
        )
        , width="auto")
        for i in range(len(titles))]),
    )
    #className='container-fluid')
    return output

def index_page(path):
    
    return html.Div([
                dbc.Jumbotron(
                [
                    html.H1("Social Media Analytics", className="display-3"),
                    html.P(
                        "We scan social media to understand what drives the topics You care about",
                        className="lead",
                    ),
                    title_card(links_twt,titles_twt, heads_twt, pars_twt, cols_twt),
                    ]),
                dbc.Jumbotron(
                [
                    html.H1("Financial News", className="display-3"),
                    html.P(
                        "Analysing news from the web with financial impact",
                        className="lead",
                    ),
                    title_card(links_nws,titles_nws, heads_nws, pars_nws, cols_nws, size="40rem", pattern=''),
                    ]),
                ]
            )
'''

index_page = html.Div([
    dcc.Link('Twitter: #AI', href='/dashboards/AI'),
    html.Br(),
    dcc.Link('Twitter: #COFFEE', href='/COFFEE'),
    html.Br(),
    dcc.Link('Twitter: #TEA', href='/TEA'),
    html.Br(),
    dcc.Link('Twitter: #FERTILITY', href='/FERTILITY'),
    html.Br(),
    dcc.Link('Twitter: #MINDSET', href='/MINDSET'),
    html.Br(),
    dcc.Link('Twitter: #FOOD', href='/FOOD'),
    html.Br(),
    dcc.Link('News', href='/NEWS'),
])
'''