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
    home_shadow, away_shadow = None, None
    
    if home_score is not None and away_score is not None:
        if home_score > away_score:
            home_color = "green"
            away_color = "red"
            home_shadow = "drop-shadow(0px 0px 20px green)"
        elif home_score < away_score:
            home_color = "red"
            away_color = "green"
            away_shadow = "drop-shadow(0px 0px 20px green)"
        elif home_score == away_score:
            home_color = "blue"
            away_color = "blue"
            
    utc_game_time = datetime.datetime.strptime(game.get("startTimeUTC"), "%Y-%m-%dT%H:%M:%SZ")
    eastern_offset = datetime.datetime.strptime(game.get("easternUTCOffset"), "-%H:%M").time()

    game_time = utc_game_time - datetime.timedelta(hours=eastern_offset.hour, minutes=eastern_offset.minute)
    
    score_bug = html.Div()
    # game hasn't started yet
    if game.get("gameState") == "FUT":
        score_bug = html.H6(f"Start Time: {game_time.strftime('%H')}:{game_time.strftime('%M')} ET", style={"display": "flex", "justifyContent": "center", "paddingTop": "5%"})
    # pre-game - game starting soon
    elif game.get("gameState") == "PRE":
        score_bug = html.Div(
            [
                html.I(className="fas fa-exclamation-circle fa-xs", style={"color": "darkgoldenrod"}),
                html.H6("Game Starting Soon!", style={"color": "darkgoldenrod", "paddingLeft": "1%"})
            ],
            style={"display": "flex", "justifyContent": "center", "alignItems": "baseline", "paddingTop": "5%"}
        )
    # game in progress
    elif game.get("gameState") == "LIVE":
        time_text = f"End Period {game.get('period')}" if game.get("clock").get("inIntermission") else f"P{game.get('period')} | {game.get('clock').get('timeRemaining')}"
        score_bug = html.Div(
            [
                html.Div(
                    [
                        html.I(className="fas fa-circle-dot fa-xs", style={"color": "red"}),
                        html.H6("Live", style={"color": "red", "paddingLeft": "1%"}),
                        html.H6(time_text, style={"paddingLeft": "2%", "color": "blue"})
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
            style={"paddingTop": "3%"}
        )
    # gameState cycles through several states on game startup & end: FUT -> PRE -> LIVE -> CRIT -> FINAL -> OFF
    # assume if game isn't live or yet to start then it is finished
    else:
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
                    html.Img(src=game.get("homeTeam").get("logo"), style={"maxWidth": 100, "filter": home_shadow}),
                    html.Img(src=game.get("awayTeam").get("logo"), style={"maxWidth": 100, "filter": away_shadow}),
                ],
                style={"display": "flex", "justifyContent": "space-evenly"}
            ),
            score_bug
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
            html.H3("Today's Games:", style={"display": "flex", "justifyContent": "center", "paddingTop": "2%"}),
            html.H3(datetime.date.today(), style={"display": "flex", "justifyContent": "center"}),
            html.Div(
                add_game_rows(games),
                id="scores-container",
            ),
            dcc.Interval(
                id='score-interval',
                interval=60 * 1000, # in milliseconds
            ),
        ],
        style={"backgroundColor": "lightgrey", "height": "100vh"}
    )


@callback(
    Output("scores-container", "children"),
    Output("score-interval", "interval"),
    Input("score-interval", "n_intervals")
)
def refresh_scores(n_intervals):
    games = requests.get(api_root + f"v1/score/{datetime.date.today()}").json().get("games")
    
    interval = 60 * 1000
    try:
        current_time = datetime.datetime.utcnow()
        
        # delay interval refresh if starting server on day of games
        # start refreshing ~10 min before first game of day
        if games[0].get("gameState") == "FUT":
            start_time = datetime.datetime.strptime(games[0].get("startTimeUTC"), "%Y-%m-%dT%H:%M:%SZ")
            
            time_diff = start_time - current_time - datetime.timedelta(minutes=10)
            interval = time_diff.total_seconds() * 1000
                        
        # no need to keep requesting api data between game days with potential 12+ hours between game times
        # change interval update time to refresh ~ 6:00 AM ET to initial load games for the day
        elif games[-1].get("gameState") == "OFF":
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            start_time = datetime.datetime.strptime(f"{tomorrow}T11:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

            time_diff = start_time - current_time
            interval = time_diff.total_seconds() * 1000
        
    except IndexError:
        pass
            
    return add_game_rows(games), interval
