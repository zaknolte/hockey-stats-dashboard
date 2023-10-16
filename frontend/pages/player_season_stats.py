import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import aiohttp
import asyncio
import base64
import pandas as pd
import numpy as np
from django.utils.text import slugify
from pathlib import Path
from io import StringIO

# from app import DJANGO_ROOT
from helpers import stringify_season

dash.register_page(__name__, path="/players")

# path that stores player images
# /backend/images/
DJANGO_ROOT = Path(__file__).resolve().parent.parent.parent / "backend"
img_path = "/".join([i for i in DJANGO_ROOT.parts])

PLAYER_STATS = ["Goals", "Assists", "Points"]


async def query_player_stats(endpoint):
    async with aiohttp.ClientSession() as session:
        api_url = f"http://127.0.0.1:8000/api/players/{endpoint}"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


CURRENT_SEASON = asyncio.run(query_player_stats("current_season"))["season"]
STRING_CURRENT_SEASON = stringify_season(CURRENT_SEASON)
ALL_SEASONS = [stringify_season(season["season"])for season in asyncio.run(query_player_stats("all_seasons"))]
ALL_SEASON_TYPES = [k for k in asyncio.run(query_player_stats("all_season_types"))]


# can't host static images in dash normally outside assets folder
# encode and decode from image url to render image
def format_image(image_url):
    encoded = base64.b64encode(open(img_path + image_url, "rb").read())
    return encoded.decode()


def build_query_url(season=CURRENT_SEASON, season_type="Regular Season", team="All Teams"):
    return f"?season={season}&season_type={season_type}&team_name={team}"

def filter_data_by_position(df, position):
    filter_list = ["C", "RW", "LW"]
    
    if position == "Defense":
        filter_list = ["RD", "LD"]
    elif position == "Goalie":
        filter_list = ["G"]
    
    return df[df["player.position"].apply(lambda x: bool(set(x) & set(filter_list)))]


def query_to_formatted_df(query):
    def split_player_position_col(x):
        vals = []
        for i in x:
            vals.append(i["position_display"])
        return vals
    
    df = pd.json_normalize(asyncio.run(query_player_stats(query))).set_index("id")
    # player.positions queried as list of dicts
    # reduce player.positions to just a list of dict values
    df["player.position"] = df["player.position"].apply(split_player_position_col)
    return df
    

def get_all_teams(df, add_all=True):
    teams_list = pd.unique(df["player.team_name"])
    teams_list.sort()
    if add_all:
        teams_list = np.insert(teams_list, 0, "All Teams")

    return teams_list


def get_filter_dropdowns_layout(df):
    all_teams = get_all_teams(df)

    return html.Div(
        [
            dcc.Dropdown(
                options=ALL_SEASONS,
                value=STRING_CURRENT_SEASON,
                style={"width": 500},
                clearable=False,
                searchable=False,
                id="dropdown-season",
            ),
            dcc.Dropdown(
                options=ALL_SEASON_TYPES,
                value="Regular Season",
                style={"width": 500},
                clearable=False,
                searchable=False,
                id="dropdown-season-type",
            ),
            dcc.Dropdown(
                options=all_teams,
                value="All Teams",
                style={"width": 500},
                clearable=False,
                searchable=False,
                id="dropdown-team",
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-around",
            "paddingTop": 50,
        },
    )


def get_league_leaders_layout(df):
    layouts = html.Div(
        [
            get_leaders_layout(df, "goals", dropdown_id=1),
            get_leaders_layout(df, "assists", dropdown_id=2),
            get_leaders_layout(df, "points", dropdown_id=3),
        ],
        style={"display": "flex", "justifyContent": "space-around"},
    )
    return layouts


def get_leaders_layout(df, stat, dropdown_id):
    rows = get_leaders_layout_rows(df, stat)

    return html.Div(
        [
            dcc.Dropdown(
                options=PLAYER_STATS,
                value=stat.title(),
                clearable=False,
                searchable=False,
                id=f"dropdown-leader-stat-{dropdown_id}",
            ),
            html.Div(
                [
                    dbc.Container(rows, id=f"rows-leader-stat-{dropdown_id}"),
                ],
            ),
        ],
        style={"width": "15%"},
    )


def get_leaders_layout_rows(df, stat):
    # filter for forwards only on initial load
    leaders = filter_data_by_position(df)
    leaders = leaders.sort_values(stat, ascending=False).head(10)
    
    # loop through players stats and generate rows and columns of results
    return [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Link(
                        value["player.full_name"],
                        href=f'player/{slugify(value["player.full_name"])}',
                    ),
                    width=8,
                ),
                dbc.Col(
                    value[stat], style={"display": "flex", "justifyContent": "end"}
                ),
            ]
        )
        for row, value in leaders[["player.full_name", stat]].iterrows()
    ]


def layout():
    # get database data with defaults for current regular season for all teams
    players_df = query_to_formatted_df(build_query_url())
    return html.Div(
        [
            get_filter_dropdowns_layout(players_df),
            html.Div(
                [
                    html.H2(
                        ["Season Leaders"],
                        style={
                            "display": "flex",
                            "justifyContent": "center",
                            "paddingTop": 50,
                        },
                    ),
                    html.H3(
                        ["Forwards"],
                        style={
                            "display": "flex",
                            "justifyContent": "center",
                            "paddingTop": 25,
                        },
                        id="player-position-label"
                    ),
                    html.Div(
                        [
                            dcc.Dropdown(
                                options=["All Positions", "C", "RW", "LW"],
                                value="All Positions",
                                searchable=False,
                                clearable=False,
                                style={"minWidth": "15%"},
                                id="player-position-dropdown"
                            ),
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "paddingTop": 15,
                            "paddingBottom": 15,
                        },
                        id="player-position-dropdown-container"
                    )
                ]
            ),
            get_league_leaders_layout(players_df),
            dcc.Store(data=players_df.to_json(), id="season-stats-df"),
        ]
    )


# generate callbacks for each stat 'column' for league leaders
for i in range(1, 4):
    @callback(
        Output(f"rows-leader-stat-{i}", "children"),
        Input(f"dropdown-leader-stat-{i}", "value"),
        Input("season-stats-df", "data"),
        prevent_initial_call=True,
    )
    def update_leader_stat_1(stat, data):
        df = pd.read_json(StringIO(data))
        return get_leaders_layout_rows(df, stat.lower())


@callback(
    Output("season-stats-df", "data"),
    Input("dropdown-season", "value"),
    Input("dropdown-season-type", "value"),
    Input("dropdown-team", "value"),
    Input("player-position-dropdown", "value"),
    prevent_initial_call=True
)
def update_displayed_data(season, season_type, team, position):
    formatted_season = int(season[:4])
    df = query_to_formatted_df(build_query_url(formatted_season, season_type, team))
    
    if position != "All Positions":
        # players may be assigned more than one position
        # create bool mask to determine if selected position matches any of the player positions
        mask = df["player.position"].apply(lambda x: position in x)
        
        df = df[mask]
    
    return df.to_json()