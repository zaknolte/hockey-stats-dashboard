import dash
from dash import html

dash.register_page(__name__, path="/players")

layout = html.Div(
    [
        html.H1("player stats go here"),
    ]
)
