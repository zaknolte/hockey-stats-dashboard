import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

import aiohttp
import asyncio
import base64
import pandas as pd
import numpy as np

from django.utils.text import slugify
from pathlib import Path
from io import StringIO

# from app import DJANGO_ROOT
from helpers import stringify_season, ag_grid_cols_rename, ag_grid_cols_reorder, update_ag_grid_display_cols

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


def get_player_options(position):  
    player_options = None
    
    if position == "Forwards":
        player_options = ["C", "RW", "LW"]
    elif position == "Defense":
        player_options = ["RD", "LD"]
    elif position == "All Positions" or position == "All Skaters":
        player_options = ["C", "RW", "LW", "RD" ,"LD"]
    elif position == "Goalies":
        player_options = ["G"]
            
    return player_options or [position]
    

def filter_data_by_position(df, position):
    filter_list = get_player_options(position)
    # find the set union where player position in contained in filter list
    return df[df[ag_grid_cols_rename["player.position"]].apply(lambda x: bool(set(x) & set(filter_list)))]


def query_to_formatted_df(query):
    def split_player_position_col(x):
        vals = []
        for i in x:
            vals.append(i["position_display"])
        return vals
    
    df = pd.json_normalize(asyncio.run(query_player_stats(query))).set_index("id")
    df = df.rename(columns=ag_grid_cols_rename)
    # Positions queried as list of dicts
    # reduce Positions to just a list of dict values
    df[ag_grid_cols_rename["player.position"]] = df[ag_grid_cols_rename["player.position"]].apply(split_player_position_col)
    return df
    

def get_all_teams(df, add_all=True):
    teams_list = pd.unique(df[ag_grid_cols_rename["player.team_name"]])
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
    

def get_player_position_groups_layout():
    return dbc.RadioItems(
        [
            {"label": "All Skaters", "value": "All Skaters"},
            {"label": "Forwards", "value": "Forwards"},
            {"label": "Defense", "value": "Defense"},
            {"label": "Goalies", "value": "Goalies"},
        ],
        style={
            "display": "flex",
            "justifyContent": "center",
            "paddingTop": 25,
        },
        id="player-position-groups",
        input_class_name="btn-check",
        label_class_name="btn btn-outline-primary",
        value="All Skaters"
    )
    

def get_player_position_options_layout():
    return dbc.RadioItems(
        [
            {"label": "All Positions", "value": "All Positions"},
            {"label": "C", "value": "C"},
            {"label": "RW", "value": "RW"},
            {"label": "LW", "value": "LW"},
        ],
        style={
            "display": "flex",
            "justifyContent": "center",
            "paddingTop": 15,
            "paddingBottom": 15,
        },
        id="player-position-options",
        input_class_name="btn-check",
        label_class_name="btn btn-outline-primary",
        value="All Positions"
    )


def get_agGrid_layout(df):
    columnDefs = [{"field": i} for i in update_ag_grid_display_cols(df).columns]
    return dag.AgGrid(
        rowData=df.to_dict("records"),
        columnDefs=columnDefs,
        id="player-stats-grid",
        style={"paddingLeft": 50, "paddingRight": 50}
    )


def get_league_leaders_layout(df, stats_list):
    layouts = html.Div(
        [
            get_leaders_layout(df, stats_list[0], dropdown_id=1),
            get_leaders_layout(df, stats_list[1], dropdown_id=2),
            get_leaders_layout(df, stats_list[2], dropdown_id=3),
        ],
        style={"display": "flex", "justifyContent": "space-around", "minHeight": 350},
    )
    return layouts


def get_leaders_layout(df, stat, dropdown_id):
    # filter for forwards only on initial load
    rows = get_leaders_layout_rows(df, stat, "Forward")

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


def get_leaders_layout_rows(df, stat, position):
    leaders = filter_data_by_position(df, position)
    leaders = leaders.sort_values(stat, ascending=False).head(10)
    
    # loop through players stats and generate rows and columns of results
    return [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Link(
                        value[ag_grid_cols_rename["player.full_name"]],
                        href=f'player/{slugify(value[ag_grid_cols_rename["player.full_name"]])}',
                    ),
                    width=8,
                ),
                dbc.Col(
                    value[stat], style={"display": "flex", "justifyContent": "end"}
                ),
            ]
        )
        for row, value in leaders[[ag_grid_cols_rename["player.full_name"], stat]].iterrows()
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
                    get_player_position_groups_layout(),
                    get_player_position_options_layout(),
                ]
            ),
            get_league_leaders_layout(players_df, ["goals", "assists", "points"]),
            get_agGrid_layout(players_df),
            dcc.Store(data=players_df.to_json(), id="season-stats-df"),
        ]
    )


@callback(
    Output("season-stats-df", "data"),
    Input("dropdown-season", "value"),
    Input("dropdown-season-type", "value"),
    Input("dropdown-team", "value"),
    Input("player-position-options", "value"),
    State("player-position-groups", "value"),
    prevent_initial_call=True
)
def update_displayed_data(season, season_type, team, position, position_group):
    formatted_season = int(season[:4])
    df = query_to_formatted_df(build_query_url(formatted_season, season_type, team))
    
    df = filter_data_by_position(df, position_group)
    
    if position != "All Positions":
        # players may be assigned more than one position
        # create bool mask to determine if selected position matches any of the player positions
        mask = df[ag_grid_cols_rename["player.position"]].apply(lambda x: position in x)
        
        df = df[mask]
    
    return df.to_json()


@callback(
    Output("player-position-options", "options"),
    Output("player-position-options", "value"),
    Input("player-position-groups", "value"),
    prevent_initial_call=True
)
def update_player_position_options(player_group):
    options =  ["All Positions"] + get_player_options(player_group)
    value = options[0]
    return options, value


@callback(
    Output("rows-leader-stat-1", "children"),
    Output("rows-leader-stat-2", "children"),
    Output("rows-leader-stat-3", "children"),
    Output("player-stats-grid", "rowData"),
    Input("dropdown-leader-stat-1", "value"),
    Input("dropdown-leader-stat-2", "value"),
    Input("dropdown-leader-stat-3", "value"),
    Input("player-position-options", "value"),
    Input("season-stats-df", "data"),
    # prevent_initial_call=True,
)
def update_leader_stats(stat_left, stat_center, stat_right, player_position, data):
    df = pd.read_json(StringIO(data))

    left = get_leaders_layout_rows(df, stat_left.lower(), player_position)
    center = get_leaders_layout_rows(df, stat_center.lower(), player_position)
    right = get_leaders_layout_rows(df, stat_right.lower(), player_position)
    
    df = update_ag_grid_display_cols(df)
    return left, center, right, df.to_dict("records")