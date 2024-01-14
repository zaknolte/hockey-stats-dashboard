from dash import html

def player_404_layout(status, player_id):
    h1_text = status
    if status == 422:
        h1_text = f"{status}: Invalid player ID entered."
    elif status == 404:
        h1_text = f"{status}: Sorry, player ID {player_id} could not be found."
        
    return html.Div(
        [
            html.H1(h1_text, style={"marginTop": "5%", "display": "flex", "justifyContent": "center"}),
            html.H3("Please enter a valid player ID or", style={"marginTop": "5%", "display": "flex", "justifyContent": "center"}),
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