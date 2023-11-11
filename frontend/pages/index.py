import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import requests
import datetime

dash.register_page(__name__, path="/")

api_root = "https://api-web.nhle.com/"

games = requests.get(api_root + f"v1/schedule/{datetime.date.today()}").json().get("gameWeek")[0].get("games")


def get_vs_card(game):
    utc_game_time = datetime.datetime.strptime(game.get("startTimeUTC"), "%Y-%m-%dT%H:%M:%SZ")
    eastern_offset = datetime.datetime.strptime(game.get("easternUTCOffset"), "-%H:%M").time()

    game_time = utc_game_time - datetime.timedelta(hours=eastern_offset.hour, minutes=eastern_offset.minute)
    return html.Div(
        [
            html.Div(
                [
                    html.H4("Home"),
                    html.H4("Away"),
                ],
                style={"display": "flex", "justifyContent": "space-evenly"}
            ),
            html.Div(
                [
                    html.Img(src=game.get("homeTeam").get("logo"), style={"maxWidth": 100}),
                    html.Img(src=game.get("awayTeam").get("logo"), style={"maxWidth": 100}),
                ],
                style={"display": "flex", "justifyContent": "space-evenly"}
            ),
            html.H6(f"Start Time: {game_time.strftime('%H')}:{game_time.strftime('%M')} ET", style={"display": "flex", "justifyContent": "center", "paddingTop": "5%"})
        ]
    )
    
    
def add_game_rows(games):
    rows = []
    cols = []
    for i, game in enumerate(games):
        if i % 3 == 0:
            rows.append(dbc.Row(cols, style={"paddingBottom": "5%"}))
            cols = []
        cols.append(dbc.Col(get_vs_card(game)))
    
    rows.append(dbc.Row(cols, style={"paddingBottom": "5%"}))
    
    return dbc.Container(rows)
        

def layout():
    
    return html.Div(
        [
            add_game_rows(games),
        ],
        style={"backgroundColor": "lightgrey"}
    )
