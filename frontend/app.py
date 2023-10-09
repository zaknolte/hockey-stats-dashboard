import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from nav import nav


app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.LUX,
    ],
    use_pages=True,
)

app.layout = html.Div(
    [
        nav,
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
