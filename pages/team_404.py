from dash import html
from data_values import ROOT_URL

def team_404_layout(status, team_id):
    h1_text = status
    if status == 422:
        h1_text = f"{status}: Invalid team name entered."
    elif status == 404:
        h1_text = f"{status}: Sorry, {team_id} could not be found."
        
    return html.Div(
        [
            html.H1(h1_text, style={"marginTop": "5%", "display": "flex", "justifyContent": "center"}),
            html.H3("Please enter a valid team name or", style={"marginTop": "5%", "display": "flex", "justifyContent": "center"}),
            html.H3(
                [
                    "Return to the",
                    html.A("Home Page", href=f"{ROOT_URL}/", style={"marginLeft": "1rem"})
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