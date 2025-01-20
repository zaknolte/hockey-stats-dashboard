import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from helpers import slugify
import requests
import datetime
import aiohttp
import asyncio

from data_values import TEAM_BY_ABBR, ROOT_URL

dash.register_page(__name__, path="/", title="Hockey Stats")

async def get_games():
    async with aiohttp.ClientSession() as session:
        api_url = f"https://api-web.nhle.com/v1/score/{datetime.date.today()}"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data.get("games")

def get_vs_card(game:dict):
    """
    Return a series of html components to display home team, away team, and live score information from a given nhl api game.
     
    Args:
        game (dict): NHL api live single game json data from https://api-web.nhle.com/v1/score/{date}'.
 
    Returns:
        html.Div: Nested html components of live score information.
    """
    home_team = game.get("homeTeam")
    away_team = game.get("awayTeam")
    
    home_score = home_team.get("score")
    away_score = away_team.get("score")

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
            
    # nhl game times are given in UTC time
    # convert to ET
    utc_game_time = datetime.datetime.strptime(game.get("startTimeUTC"), "%Y-%m-%dT%H:%M:%SZ")
    eastern_offset = datetime.datetime.strptime(game.get("easternUTCOffset"), "-%H:%M").time()

    game_time = utc_game_time - datetime.timedelta(hours=eastern_offset.hour, minutes=eastern_offset.minute)
    
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
                        html.I(className="fas fa-circle-dot fa-2xs", style={"color": "red"}),
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
                    html.A(
                        html.Img(src=game.get("homeTeam").get("logo"), style={"width": 100, "maxWidth": 100, "filter": home_shadow}),
                        href=f"{ROOT_URL}/teams/{slugify(TEAM_BY_ABBR[home_team.get('abbrev')])}"
                    ),
                    html.A(
                        html.Img(src=game.get("awayTeam").get("logo"), style={"width": 100, "maxWidth": 100, "filter": away_shadow}),
                        href=f"{ROOT_URL}/teams/{slugify(TEAM_BY_ABBR[away_team.get('abbrev')])}"
                    )
                ],
                style={"display": "flex", "justifyContent": "space-evenly"}
            ),
            score_bug
        ]
    )
    
    
def add_game_rows(games:list):
    """
    Return a series of rows of html score bug cards from a give nhl api game date.
     
    Args:
        games (list): List of NHL api live game json data from https://api-web.nhle.com/v1/score/{date}'.
 
    Returns:
        dbc.Container: Multiple rows of dbc components of live score information.
    """
    rows = []
    cols = []
    padding_left = None
    padding_right = None
    num_cards = 1
    for i, game in enumerate(games):
        if i % 3 == 0:
            rows.append(dbc.Row(cols, style={"paddingBottom": "5%"}))
            cols = []
            num_cards = 1
            
        cols.append(dbc.Col(get_vs_card(game)))
        
        padding_left = 33 / num_cards
        padding_right = 33 / num_cards
        num_cards += 1
            
    rows.append(dbc.Row(cols, style={"paddingBottom": "5%", "paddingLeft": f"{padding_left}%", "paddingRight": f"{padding_right}%"}))
    
    return dbc.Container(rows)
        

def layout():
    games = asyncio.run(get_games())
    
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
        style={"height": "100vh"}
    )


@callback(
    Output("scores-container", "children"),
    Output("score-interval", "interval"),
    Input("score-interval", "n_intervals")
)
def refresh_scores(n_intervals):
    games = asyncio.run(get_games())
    
    interval = 60 * 1000
    try:
        current_time = datetime.datetime.utcnow()
        
        # delay interval refresh if starting refresh on day of games
        # start refreshing ~10 min before first game of day
        if games[0].get("gameState") == "FUT":
            start_time = datetime.datetime.strptime(games[0].get("startTimeUTC"), "%Y-%m-%dT%H:%M:%SZ")
            
            time_diff = start_time - current_time - datetime.timedelta(minutes=10)
            interval = time_diff.total_seconds() * 1000
                        
        # no need to keep requesting api data between game days with potential 12+ hours between game times
        # change interval update time to refresh ~ 6:00 AM ET to initially load games for the day
        elif games[-1].get("gameState") == "OFF":
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            start_time = datetime.datetime.strptime(f"{tomorrow}T11:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

            time_diff = start_time - current_time
            interval = time_diff.total_seconds() * 1000
        
    except IndexError:
        pass
            
    return add_game_rows(games), interval
