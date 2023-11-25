import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1("Sorry, this page could not be displayed.", style={"marginTop": "5%", "display": "flex", "justifyContent": "center"}),
        html.H3(
            [
                "Return to the",
                html.A("Home Page", href="http://127.0.0.1:8050/", style={"marginLeft": "1rem"})
            ],
            style={"marginTop": "5%", "display": "flex", "justifyContent": "center"}
        )
        
    ],
    style={
        "height": "100vh",
        "backgroundImage": "url('/assets/404puck.png')",
        "backgroundRepeat": "no-repeat"
        }
)