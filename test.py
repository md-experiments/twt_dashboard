import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(
    children=[
        dcc.Graph(
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                ],
            }
        )
    ],style = {"display":"grid","grid-template-columns":"1fr"}
)

if __name__ == '__main__':
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    print(dir_path)
    app.run_server(debug=True)