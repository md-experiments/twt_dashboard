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
from learning import learning_blueprint 

import pandas as pd

print(dcc.__version__) # 0.6.0 or above is required
external_stylesheets = [
    dict(
        rel="stylesheet",
        href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" ,
        integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" ,
        crossorigin="anonymous"
    )
]

#app = dash.Dash()
app = Flask(__name__)  # '__main__'
app.register_blueprint(learning_blueprint)



app_dash = Dash(__name__,
               server=app,
               url_base_pathname='/',
               external_stylesheets=external_stylesheets)


app_dash.config.suppress_callback_exceptions = True

links=['tea','coffee','food','fertility','mindset','ai']
titles=['Tea','Coffee','Food','Fertility','LifeCoach','AI']

def card(nr,link_nm,title):
    return html.Div(
        id=f'main-{nr}',
        children=[
            html.Br(),
            html.Img(src=f'/static/{link_nm}.png', className='card-img'),
            dcc.Link(f'Twitter: #{title}', href=f'/{link_nm.upper()}'),
            ],
        style={'width': '15%', 'display': 'inline-block'},
        className='card'  
    )


app_dash.layout = html.Div([
        html.Div([
        dcc.Location(id='url', refresh=True),
        html.Div(id='page-content'),
        ]),
        html.Div([card(i,links[i],titles[i]) for i in range(3)]),
        html.Div([card(i,links[i],titles[i]) for i in range(3,6)]),
        ])
app_dash.title = 'CountingChickens'



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
