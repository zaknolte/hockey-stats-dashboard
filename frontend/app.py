import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from nav import nav

from pathlib import Path

# DJANGO_ROOT = Path(__file__).resolve().parent.parent / "backend"

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
