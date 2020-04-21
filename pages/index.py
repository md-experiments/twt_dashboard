import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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