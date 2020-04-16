import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

index_page = html.Div([
    dcc.Link('Twitter: #AI', href='/AI'),
    html.Br(),
    dcc.Link('Twitter: #COFEE', href='/COFFEE'),
    html.Br(),
    dcc.Link('Twitter: #TEA', href='/TEA'),
    html.Br(),

    dcc.Link('News', href='/page-2'),
])