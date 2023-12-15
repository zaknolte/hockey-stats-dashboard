import dash
from dash import html, dcc, callback, Input, Output, State, ctx, no_update
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
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
from helpers import stringify_season, rename_data_df_cols, get_stat_sorting, get_agGrid_layout, get_agGrid_columnDefs, cols_to_percent

dash.register_page(__name__, path="/players", title="Hockey Stats | Player Stats")


async def query_player_stats(endpoint:str):
    """
    Performs an async query to the backed server and the supplied endpoint.
 
    Args:
        endpoint (str): url endpoint to query including and query params.
 
    Returns:
        json response of data.
    """
    async with aiohttp.ClientSession() as session:
        api_url = f"http://127.0.0.1:8000/api/season/{endpoint}"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


# default values
CURRENT_SEASON = asyncio.run(query_player_stats("current_season"))["season"]
STRING_CURRENT_SEASON = stringify_season(CURRENT_SEASON)
ALL_SEASONS = ["All Seasons"] + [stringify_season(season) for season in asyncio.run(query_player_stats("all_seasons"))["season"]]
ALL_SEASON_TYPES = ["Regular Season", "Playoffs"]


# can't host static images in dash normally outside assets folder
# encode and decode from image url to render image
def format_image(image_url:str):
    """
    Encodes then returns the base64 decoded image supplied from image_url
 
    Args:
        image_url (str): Path to image file.
 
    Returns:
        base64 decoded image.
    """
    # path that stores player images
    # /backend/images/
    DJANGO_ROOT = Path(__file__).resolve().parent.parent.parent / "backend"
    img_path = "/".join([i for i in DJANGO_ROOT.parts]) + "/images/player-pictures/"
    
    encoded = base64.b64encode(open(img_path + image_url, "rb").read())
    return encoded.decode()


def build_player_query_url(skater_type="skater", player_type="all", season="All Seasons", season_type="Regular Season", team="All Teams"):
    """
    
    Builds and returns a query url to query the backend database.
 
    Args:
        season (int): The year of the season start e.g. 2023 for the 2023-2024 season.
        season_type (str): The season type to query. One of 'Pre-Season', 'Regular Season', or 'Playoffs'.
        team (str): A specific team to query or 'All Teams'.
 
    Returns:
        str: The compiled endpoint url string.
    """
    return f"{skater_type}/{player_type}?season={season}&season_type={season_type}&team={team}"


def get_player_options(position:str):
    """
    Builds and returns a list of player positions depending on the given position group.
 
    Args:
        position (str): The position area. One of 'Forwards', 'Defense', 'Goalies', or 'All Positions'/'All Skaters'.
 
    Returns:
        list: The list of all positions that belong to the given position group.
    """
    player_options = None
    
    if position == "Forwards":
        player_options = ["C", "RW", "LW"]
    elif position == "Defense":
        player_options = ["RD", "LD", "D"]
    elif position == "All Positions" or position == "All Skaters":
        player_options = ["C", "RW", "LW", "RD" ,"LD", "D", "G"]
    elif position == "Goalies":
        player_options = ["G"]
            
    return player_options or [position]
    

def filter_data_by_position(df:object, position:str):
    """
    Filter and return a dataframe of only the given positions.
 
    Args:
        df (obj): Pandas dataFrame to filter.
        position (str / list[str]): The position or list of positions to filter. Can be any of 'Forwards', 'Defense', 'Goalies', 'All Positions' / 'All Skaters'.
            Or can be one of any abreviated specific position e.g. 'C', 'RD', 'G'.
 
    Returns:
        obj: The filtered dataFrame.
    """
    filter_list = get_player_options(position)
    # find the set union where player position in contained in filter list
    return df[df["Position"].apply(lambda x: bool(set(x) & set(filter_list)))]


def query_to_formatted_df(query:str):
    """
    Queries backend database for data then formats the returned data into a dataFrame.
 
    Args:
        query (str): The url endpoint to query including query params.
 
    Returns:
        obj: Formatted dataFrame of database data.
    """
    df = pd.json_normalize(asyncio.run(query_player_stats(query))).set_index("id")
    df = df.rename(columns=rename_data_df_cols)
    df["Team"] = df["Team"].fillna("N/A")
    
    df = cols_to_percent(df, "FO %")
    
    rounding = {
        "FO %": 2,
        "Save %": 3,
        "GAA": 2,
    }
    # df = df.round(rounding)
    
    # display issues with rounded floating imprecision
    # convert to string to truncate
    # if used in agGrid - grid can convert back to number with proper precision
    for i in rounding:
        try:
            df[i] = df[i].apply(lambda x: f"{x:.{rounding[i]}f}")
        except (KeyError, TypeError):
            pass

    return df
    

def get_all_teams(df:object, add_all=True):
    """
    Returns a list of all teams within a given dataFrame.
 
    Args:
        df (obj): The dataFrame to collect available team names.
        add_all (bool): If true, will insert an 'All Teams' option and the beginning of the list.
 
    Returns:
        list[str]: List of all present team names.
    """
    teams_list = pd.unique(df["Team"])
    teams_list.sort()
    if add_all:
        teams_list = np.insert(teams_list, 0, "All Teams")

    return teams_list


def get_leaders_dropdown_options(position="All Skaters"):
    """
    Returns a list of stat name options for filtering the dataset and returning the top 10 leaders.
 
    Args:
        position (str): The position used to return a list of stats specific for that position.
 
    Returns:
        list[str]: List of stat names for a given position.
    """
    options = []
    ignore = [
        "id",
        "Player",
        "Season",
        "Full Season",
        "Team",
        "Position"
    ]
    for col in get_agGrid_columnDefs(position):
        if col["field"] not in ignore:
            options.append(col["field"])
            
    return options

def get_filter_dropdowns_layout(seasons:list[str], season_types:list[str], teams:list[str]):
    """
    Return list of 3 dcc.Dropdown components. Creates dropdowns for seasons, season types, and team names used for filtering data.
 
    Args:
        seasons (list[str]): List of all available seasons to add as options for dropdown.
        season_types (list[str]): The season type to add as options for dropdown. Should be list of ['Pre-Season', 'Regular Season', 'Playoffs'].
        teams (list[str]): List of all teams to add as options for dropdown.
 
    Returns:
        obj: html.Div containing dcc.Dropdowns.
    """
    return html.Div(
        [
            dcc.Dropdown(
                options=seasons,
                value=STRING_CURRENT_SEASON,
                clearable=False,
                searchable=False,
                id="dropdown-season",
                style={"width": 500},
            ),
            dcc.Dropdown(
                options=season_types,
                value="Regular Season",
                clearable=False,
                searchable=False,
                id="dropdown-season-type",
                style={"width": 500},
            ),
            dcc.Dropdown(
                options=teams,
                value="All Teams",
                clearable=False,
                searchable=False,
                id="dropdown-team",
                style={"width": 500},
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-around",
            "paddingTop": 50,
        },
        id="player-filter-dropdowns"
    )
    

def get_player_position_groups_layout():
    """
    Return stylized dbc.RadioItems for all player position groups: 'All Skaters', 'Forwards', 'Defense', 'Goalies'.
 
    Args:
        None.
 
    Returns:
        obj: dbc.RadioItems.
    """
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
    """
    Return stylized dbc.RadioItems for all specific player positions e.g. 'C', 'RD', 'G', etc..
 
    Args:
        None.
 
    Returns:
        obj: dbc.RadioItems.
    """
    return dbc.RadioItems(
        [
            {"label": "All Positions", "value": "All Positions"},
            {"label": "C", "value": "C"},
            {"label": "RW", "value": "RW"},
            {"label": "LW", "value": "LW"},
            {"label": "RD", "value": "RD"},
            {"label": "LD", "value": "LD"},
            {"label": "D", "value": "D"},
            {"label": "G", "value": "G"},
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


def get_league_leaders_layout(df:object, stats_list:list[str]):
    """
    Return nested Div of dropdown and row data of top 10 players for chosen filtered df.
    DOM tree of: 
    
    ->html.Div(
            html.Div(
                [
                    dbc.Dropdown()
                    
                    html.Div(
                        dbc.Container(
                            dbc.Row()
                        )
                    )
                ]
            )
    )
 
    Args:
        df (obj): dataFrame of filtered data to collect top 10 of selected stat.
        stats_list (list[str]): The list of 3 stats to display for league leaders.
 
    Returns:
        obj: html.Div containing stat dcc.Dropdown with dbc.Rows of player data.
    """
    layouts = html.Div(
        [
            get_leaders_layout(df, stats_list[0], dropdown_id=1),
            get_leaders_layout(df, stats_list[1], dropdown_id=2),
            get_leaders_layout(df, stats_list[2], dropdown_id=3),
        ],
        style={"display": "flex", "justifyContent": "space-around", "minHeight": 350},
    )
    return layouts


def get_leaders_layout(df:object, stat:str, dropdown_id:int | str):
    """
    Return nested Div of dropdown and row data of top 10 players for chosen filtered df.
    DOM tree of: 
    
    html.Div(
            ->html.Div(
                [
                    dbc.Dropdown()
                    
                    html.Div(
                        dbc.Container(
                            dbc.Row()
                        )
                    )
                ]
            )
    )
 
    Args:
        df (obj): dataFrame of filtered data to collect top 10 of selected stat.
        stat (str): dataFrame stat to display leaders for.
        dropdown_id (int | str): Used to set the id property of the dcc.Dropdown used for callbacks.
 
    Returns:
        obj: html.Div containing stat dcc.Dropdown with dbc.Rows of player data.
    """
    rows = get_leaders_layout_rows(df, stat)
    player_options = get_leaders_dropdown_options("All Skaters")

    return html.Div(
        [
            dcc.Dropdown(
                options=player_options,
                value=stat.title(),
                clearable=False,
                searchable=False,
                id=f"dropdown-leader-stat-{dropdown_id}",
            ),
            html.Div(
                [
                    dls.DualRing(dbc.Container(rows, id=f"rows-leader-stat-{dropdown_id}"), debounce=20),
                ],
            ),
        ],
        style={"width": "15%"},
    )


def get_leaders_layout_rows(df:object, stat:str):
    """
    Return nested Div of dropdown and row data of top 10 players for chosen filtered df.
    DOM tree of: 
    
    html.Div(
            html.Div(
                [
                    dbc.Dropdown()
                    
                    html.Div(
                        dbc.Container(
                            ->dbc.Row()
                        )
                    )
                ]
            )
    )
 
    Args:
        df (obj): dataFrame of filtered data to collect top 10 of selected stat.
        stat (str): dataFrame stat to display leaders for.
        position (str): Player position used to filter df and get top 10 list.
 
    Returns:
        obj: lsit of dbc.Rows of player data.
    """
    leaders = df.sort_values(stat, ascending=get_stat_sorting(stat)).head(10)
    
    # loop through players stats and generate rows and columns of results
    return [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Link(
                        value["Name"],
                        href=f'player/{slugify(value["Name"])}',
                    ),
                    width=8,
                ),
                dbc.Col(
                    value[stat], style={"display": "flex", "justifyContent": "end"}
                ),
            ]
        )
        for row, value in leaders[["Name", stat]].iterrows()
    ]


def layout():
    # get database data with defaults for current regular season for all teams
    players_df = query_to_formatted_df(build_player_query_url(season=CURRENT_SEASON)).sort_values("P", ascending=False)
    
    return html.Div(
        [
            dcc.Store(data=players_df.to_json(), id="season-stats-df"),
            get_filter_dropdowns_layout(ALL_SEASONS, ALL_SEASON_TYPES, get_all_teams(players_df)),
            html.Div(
                [
                    get_player_position_groups_layout(),
                    get_player_position_options_layout(),
                    html.H2(
                        ["Season Leaders"],
                        style={
                            "display": "flex",
                            "justifyContent": "center",
                            "paddingTop": 10,
                            "paddingBottom": 10,
                        },
                    ),
                ]
            ),
            get_league_leaders_layout(players_df, ["G", "A", "P"]),
            dls.DualRing(get_agGrid_layout(players_df, "Forwards", "player-stats-grid", style={"paddingLeft": 50, "paddingRight": 50, "paddingBottom": 50}), width=120),
        ],
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
def update_displayed_data(season:str, season_type:str, team:str, position:str, position_group:str):
    season = season.replace("-", "") if season != "All Seasons" else season.replace("-", "")
    
    if position != "G":
        df = query_to_formatted_df(build_player_query_url(skater_type="skater", season=season, season_type=season_type, team=team))
        df = df.sort_values("P", ascending=False)
    else:
        df = query_to_formatted_df(build_player_query_url(skater_type="goalie", season=season, season_type=season_type, team=team))
        df = df.sort_values("W", ascending=False)
    df = filter_data_by_position(df, position_group)
    
    if position != "All Positions":
        # players may be assigned more than one position
        # create bool mask to determine if selected position matches any of the player positions
        mask = df["Position"].apply(lambda x: position in x)
        
        df = df[mask]
    
    return df.to_json()


@callback(
    Output("player-position-options", "options"),
    Output("player-position-options", "value"),
    Input("player-position-groups", "value"),
    prevent_initial_call=True
)
def update_player_position_options(player_group:str):
    options = get_player_options(player_group)
    
    if player_group != "Goalies":
        options.insert(0, "All Positions")
        
    value = options[0]
    return options, value


@callback(
    Output("dropdown-leader-stat-1", "options"),
    Output("dropdown-leader-stat-2", "options"),
    Output("dropdown-leader-stat-3", "options"),
    Output("dropdown-leader-stat-1", "value"),
    Output("dropdown-leader-stat-2", "value"),
    Output("dropdown-leader-stat-3", "value"),
    Input("player-position-options", "value"),
    prevent_initial_call=True,
)
def update_leader_dropdown_options(position):
    if position == "G":
        values = ["W", "Save %", "GAA"]
    else:
        values = ["G", "A", "P"]
    player_options = [get_leaders_dropdown_options(position)] * 3
    return player_options + values


@callback(
    Output("player-stats-grid", "rowData"),
    Output("player-stats-grid", "columnDefs"),
    Input("player-position-options", "value"),
    Input("season-stats-df", "data"),
    prevent_initial_call=True,
)
def update_agGrid(player_position:str, data:object):
    df = pd.read_json(StringIO(data))
        
    df = df.rename(columns=rename_data_df_cols)
    rowData = df.to_dict("records")
    columnDefs = get_agGrid_columnDefs(player_position)

    return rowData, columnDefs


@callback(
    Output("rows-leader-stat-1", "children"),
    Input("dropdown-leader-stat-1", "value"),
    Input("season-stats-df", "data"),
    prevent_initial_call=True,
)
def update_left_leader_stats(stat_left:str, data:object):
    df = pd.read_json(StringIO(data))
    
    left = get_leaders_layout_rows(df, stat_left)

    return left


@callback(
    Output("rows-leader-stat-2", "children"),
    Input("dropdown-leader-stat-2", "value"),
    Input("season-stats-df", "data"),
    prevent_initial_call=True,
)
def update_center_leader_stats(stat_center:str, data:object):
    df = pd.read_json(StringIO(data))
    
    center = get_leaders_layout_rows(df, stat_center)

    return center


@callback(
    Output("rows-leader-stat-3", "children"),
    Input("dropdown-leader-stat-3", "value"),
    Input("season-stats-df", "data"),
    prevent_initial_call=True,
)
def update_right_leader_stats(stat_right:str, data:object):
    df = pd.read_json(StringIO(data))
    
    right = get_leaders_layout_rows(df, stat_right)

    return right