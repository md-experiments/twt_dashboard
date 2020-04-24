import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import os

links=['TEA','COFFEE','FOOD','FERTILITY','MINDSET','AI']
titles=['Tea','Coffee','Food','Fertility','LifeCoach','AI']

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=os.path.join(os.getcwd(), '/assets/logo.png'), height="30px")),
                    dbc.Col(dbc.NavbarBrand("CountingChickens", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
        [dbc.DropdownMenu(
            children=
                [dbc.DropdownMenuItem("Twitter", header=True),]+
                [dbc.DropdownMenuItem(f"#{title}", href=f"/dashboards/{link}", external_link=True) for link,title in zip(links,titles)]
                ,
            nav=True,
            in_navbar=True,
            label="Twitter",
        ),
        dbc.DropdownMenu(
            children=
                [dbc.DropdownMenuItem("News", header=True),]+
                [
                    dbc.DropdownMenuItem(f"Macro", href=f"/dashboards/MACRO", external_link=True),
                    dbc.DropdownMenuItem(f"Company", href=f"/dashboards/COMPANY", external_link=True),
                    ]
                ,
            nav=True,
            in_navbar=True,
            label="News",
        ),]
        , id="navbar-collapse", navbar=True),
    ],
    color="light",
    dark=False,
    sticky='top'
)



'''def card(nr,link_nm,title):
    return html.Div(
        id=f'main-{nr}',
        children=[
            html.Br(),
            html.Img(src=f'/static/{link_nm}.png', className='card-img'),
            html.Div(
                [dcc.Link(f'Twitter: #{title}', href=f'/dashboards/{link_nm.upper()}'),],
                className='card-img-overlay'
                )
            ],
        style={'width': '15%', 'display': 'inline-block'},
        className='card'  
    )'''

def card(links,titles, pattern):
    output=dbc.Row([dbc.Col(dbc.Card(
            id=f'main-{i}',
            children=[
                html.Img(src=os.path.join(os.getcwd(), f'/assets/{links[i].lower()}.png'), style={'width':'100%'}),
                dbc.CardBody(
                    [html.Br(), 
                    dbc.Button(f'{pattern}{titles[i]}', href=f'/dashboards/{links[i].upper()}', external_link=True, size="sm")],
                    style={'justify-content': 'flex-end',
                            'align-items': 'flex-end'},
                    className='card-img-overlay'
                    )
                ],
            style={"width": "12rem"},
        )
        , width="auto")
        for i in range(len(titles))])
    return output
