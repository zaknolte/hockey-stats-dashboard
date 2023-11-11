import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import requests
import datetime

dash.register_page(__name__, path="/", title="Hockey Stats")

api_root = "https://api-web.nhle.com/"


def get_vs_card(game):
    home_score = game.get("homeTeam").get("score")
    away_score = game.get("awayTeam").get("score")
    home_color, away_color = "black", "black"
    
    if home_score is not None and away_score is not None:
        if home_score > away_score:
            home_color = "green"
            away_color = "red"
        elif home_score < away_score:
            home_color = "red"
            away_color = "green"
        elif home_score == away_score:
            home_color = "blue"
            away_color = "blue"
            
    utc_game_time = datetime.datetime.strptime(game.get("startTimeUTC"), "%Y-%m-%dT%H:%M:%SZ")
    eastern_offset = datetime.datetime.strptime(game.get("easternUTCOffset"), "-%H:%M").time()

    game_time = utc_game_time - datetime.timedelta(hours=eastern_offset.hour, minutes=eastern_offset.minute)
    
    score_bug = html.H6(f"Start Time: {game_time.strftime('%H')}:{game_time.strftime('%M')} ET", style={"display": "flex", "justifyContent": "center", "paddingTop": "5%"})
    
    if game.get("gameState") == "FINAL" or game.get("gameState") == "OFF":
        score_bug = html.Div(
            [
                html.Div(html.H6("FINAL"), style={"display": "flex", "justifyContent": "center"}),
                html.Div(
                    [
                        html.H4(home_score, style={"color": home_color}),
                        html.H4(away_score, style={"color": away_color}),
                    ],
                    style={"display": "flex", "justifyContent": "space-evenly"}
                ),
            ],
            style={"paddingTop": "2%"}
        )
    elif game.get("gameState") == "LIVE":
        score_bug = html.Div(
            [
                html.Div(
                    [
                        html.I(className="fas fa-circle-dot fa-xs", style={"color": "red"}),
                        html.H6("Live", style={"color": "red", "paddingLeft": "1%"}),
                        html.H6(f"P{game.get('period')} | {game.get('clock').get('timeRemaining')}", style={"paddingLeft": "2%", "color": "blue"})
                    ],
                    style={"display": "flex", "justifyContent": "center", "alignItems": "baseline"}
                ),
                html.Div(
                    [
                        html.H4(home_score, style={"color": home_color}),
                        html.H4(away_score, style={"color": away_color}),
                    ],
                    style={"display": "flex", "justifyContent": "space-evenly"}
                )
            ],
            style={"paddingTop": "2%"}
        )

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
            score_bug,
            dcc.Interval(
                id='score-interval',
                interval=60*1000, # in milliseconds
            )
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
    games = requests.get(api_root + f"v1/score/{datetime.date.today()}").json().get("games")
    
    return html.Div(
        [
            add_game_rows(games),
        ],
        id="scores-container",
        style={"backgroundColor": "lightgrey"}
    )


@callback(
    Output("scores-container", "children"),
    Input("score-interval", "n_intervals")
)
def refresh_scores(n_intervals):
    games = requests.get(api_root + f"v1/score/{datetime.date.today()}").json().get("games")
    return add_game_rows(games)