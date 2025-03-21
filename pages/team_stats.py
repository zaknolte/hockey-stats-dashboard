import dash
from dash import html, dcc, callback, Input, Output, State, Patch
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
import dash_ag_grid as dag
import plotly.graph_objs as go

import aiohttp
import asyncio
import base64
import pandas as pd
import requests
import numpy as np

from helpers import slugify
from pathlib import Path
from io import StringIO

from data_values import TEAM_COLORS, BACKEND_URL
from helpers import reverse_slugify, rename_data_df_cols, cols_to_percent, get_colors, get_triadics_from_rgba, get_rgba_complement, get_agGrid_layout, stringify_season
from .team_404 import team_404_layout


def title(team):
    return f"Hockey Stats | {team.replace('-', ' ').title()}"


dash.register_page(__name__, path_template="/teams/<team>", title=title)


async def query_team_stats(endpoint):
    """
    Performs an async query to the backed server and the supplied endpoint.

    Args:
        endpoint (str): url endpoint to query including and query params.

    Returns:
        json response of data.
    """
    async with aiohttp.ClientSession() as session:
        api_url = f"{BACKEND_URL}/api/{endpoint}"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


def get_response(query):
    try:
        response = asyncio.run(query_team_stats(query))
    except aiohttp.client_exceptions.ContentTypeError:
        return (422, None)
    
    try:
        if "Not Found" in response["detail"]:
            return (404, None)
    except (KeyError, TypeError):
        return (200, response)


def create_formatted_df(response, index=None, sort_by=None, ascending=False):
    """
    Queries backend database for data then formats the returned data into a dataFrame.

    Args:
        query (str): The url endpoint to query including query params.

    Returns:
        obj: Formatted dataFrame of database data.
    """
    df = pd.json_normalize(response)
    
    if index is not None:
        df= df.set_index(index)

    df = df.rename(columns=rename_data_df_cols)
    if sort_by is not None:
        df = df.sort_values(sort_by, ascending=ascending)
    
    df = cols_to_percent(df, ["FO %", "Save %", "PP %", "PK %", "Shot %"])
        
    rounding = {
        "G/G": 2,
        "GA/G": 2,
        "FO %": 2,
        "PP %": 2,
        "PK %": 2,
        "Save %": 2,
        "Shot %": 2,
        "Shots/G": 2,
        "Shots Against/G": 2,
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


def build_team_query_url(endpoint:str, **kwargs):
    """
    Builds and returns a query url to query the backend database.

    Args:
        season (int): The year of the season start e.g. 2023 for the 2023-2024 season.
        season_type (str): The season type to query. One of 'Pre-Season', 'Regular Season', or 'Playoffs'.
        team (str): A specific team to query or 'All Teams'.

    Returns:
        str: The compiled endpoint url string.
    """
    query_params = "&".join([f"{i}={kwargs[i]}" for i in kwargs])
    
    return f"{endpoint}?{query_params}"


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
    img = requests.get(image_url)
    uri = ("data:" + img.headers['Content-Type'] + ";base64," + str(base64.b64encode(img.content).decode("utf-8")))
    return uri


def get_team_card(team_data:object):
    """
    Build and return a card of general team information including logo, division, conference, and inagural season.

    Args:
        team_data (DataFrame): DataFrame data of a given team.

    Returns:
        html.Div: Card component of team information.
    """
    logo = team_data["team.logo"]
    return html.Div(
        dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.CardImg(
                                src=format_image(logo),
                                className="img-fluid rounded-start",
                                style={"width": 200}
                            ),
                            className="col-md-5",
                        ),
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4(team_data["Team"], className="card-title"),
                                    html.Div(
                                        [
                                            html.B("Conference:", style={"fontWeight": "bold", "paddingRight": 5}),
                                            html.P(team_data["team.conference"])
                                        ],
                                        className="card-text",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.B("Division:", style={"fontWeight": "bold", "paddingRight": 5}),
                                            html.P(team_data["team.division"])
                                        ],
                                        className="card-text",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.B("Inagural Season:", style={"fontWeight": "bold", "paddingRight": 5}),
                                            html.P(stringify_season(team_data["team.start_season"]))
                                        ],
                                        className="card-text",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.P(f"{team_data['team.city']}, {team_data['team.state']}")
                                        ],
                                        className="card-text",
                                    ),
                                ]
                            ),
                            className="col-md-7",
                            style={"paddingLeft": 10, "color": "white"}
                        ),
                    ],
                    className="g-0 d-flex align-items-center",
                )
            ],
            className="mb-3 border-0 bg-transparent",
            style={"maxWidth": "540px", "paddingTop": 10},
        ),
        style={"display": "flex", "justifyContent": "center"}
    )


def get_season_summary(team_data:object, layout_id:[int, str]):
    """
    Return a list of dbc.Rows containing general season stats for a given team.

    Args:
        team_data (DataFrame): DataFrame data of a given team.
        layout_id (int, str): Ids applied to each season stat component used to sync data with a tooltip.

    Returns:
        list: dbc.Rows of season stat headers and data synced with tooltip information.
    """
    col_style = {"border": 1, "borderRightStyle": "solid", "display": "flex", "justifyContent": "center"}
    return [
            dbc.Row(
                [
                    dbc.Col("Season", width={"size": 1, "offset": 2}, style=col_style),
                    dbc.Col("GP", width=1, style=col_style, id=f"games-played-tooltip-{layout_id}"),
                    dbc.Col("W", width=1, style=col_style, id=f"wins-tooltip-{layout_id}"),
                    dbc.Col("L", width=1, style=col_style, id=f"losses-tooltip-{layout_id}"),
                    dbc.Col("ROW", width=1, style=col_style, id=f"row-tooltip-{layout_id}"),
                    dbc.Col("OTL", width=1, style=col_style, id=f"otl-tooltip-{layout_id}"),
                    dbc.Col("P", width=1, style=col_style, id=f"points-tooltip-{layout_id}"),
                    dbc.Col("Rank", width=1, style=col_style),
                ],
                style={"color": "white"}
            ),
            dbc.Row(
                [
                    dbc.Col(stringify_season(team_data["Season"]), width={"size": 1, "offset": 2}, style=col_style),
                    dbc.Col(team_data["GP"], width=1, style=col_style),
                    dbc.Col(team_data["W"], width=1, style=col_style),
                    dbc.Col(team_data["L"], width=1, style=col_style),
                    # TODO add ROW data to model
                    dbc.Col("0", width=1, style=col_style),
                    dbc.Col(team_data["OTL"], width=1, style=col_style),
                    dbc.Col(team_data["P"], width=1, style=col_style),
                    # dbc.Col(team_data["Rank"], width=1, style=col_style),
                    dbc.Col("N/A", width=1, style=col_style),
                ],
                style={"color": "white"}
            ),
            dbc.Tooltip("Games Played", target=f"games-played-tooltip-{layout_id}", placement="top"),
            dbc.Tooltip("Wins", target=f"wins-tooltip-{layout_id}", placement="top"),
            dbc.Tooltip("Losses", target=f"losses-tooltip-{layout_id}", placement="top"),
            dbc.Tooltip("Regulation and Overtime Wins", target=f"row-tooltip-{layout_id}", placement="top"),
            dbc.Tooltip("Overtime Losses", target=f"otl-tooltip-{layout_id}", placement="top"),
            dbc.Tooltip("Points", target=f"points-tooltip-{layout_id}", placement="top"),
        ]


def get_single_season_dropdown(team_name:str, options:list, id:str):
    """
    Return a team-specific stylized dcc.Dropdown of 'options'.

    Args:
        team_name (str): Team name used to get specific colors to style dropdown.
        options (list): List of values to fill the dropdown options with.
        id (str): Id of dropdown component.

    Returns:
        dcc.Dropdown: Team color themed dropdown.
    """
    return dcc.Dropdown(
            options=options,
            value=options[0],
            clearable=False,
            searchable=False,
            id=id,
            className="team-stats team-colored-dropdown",
            style={
                "width": "200px",
                "backgroundColor": get_colors(team_name, "secondary"),
                "--team-text-color-primary": get_colors(team_name, "primary_text"),
                "--team-text-color-secondary": get_colors(team_name, "secondary_text"),
                "--team-color-primary": get_colors(team_name, "primary"),
                "--team-color-secondary": get_colors(team_name, "secondary")
            },
        )    

def get_single_season_ranks_y_values(df:object, team_name:str, stat:str, num_points=2):
    """
    Calculate and return y-value graph pairs for league min, max, avg, and team data of given stat.

    Args:
        df (DataFrame): Single season league data.
        team_name (str): Team name to get data from.
        stat (str): Specific stat to plot.
        num_points (int): Number of copies of y-data to match the number of x-points needed.

    Returns:
        tuple: team stat data, league low data, league average data, league max data.
    """
    team_data = [df[df["Team"] == team_name][stat].iloc[0]] * num_points
    lowest_data = [df[stat].min()] * num_points
    avg_data = [df[stat].mean()] * num_points
    highest_data = [df[stat].max()] * num_points
    
    return team_data, lowest_data, avg_data, highest_data


def get_single_season_rankings_plot(df:object, team_name:str, stat:str):
    """
    Return a team specific themed dcc.Graph of league season data for a given stat.

    Args:
        df (DataFrame): Single season league data.
        team_name (str): Team name to get data from and style graph colors.
        stat (str): Specific stat to plot.

    Returns:
        dcc.Graph: Team color themed graph of team data, league min, league max, and league average.
    """
    x = [0, 1] # two points to make a line - not a single point
    team_data, lowest_data, avg_data, highest_data = get_single_season_ranks_y_values(df, team_name, stat, len(x))
    
    primary_color = get_colors(team_name, "primary")
    secondary_color = get_colors(team_name, "secondary")
    secondary_text_color = get_colors(team_name, "secondary_text")
    
    raw_primary_color = TEAM_COLORS[team_name]["primary"]
    triadic_primary_one, triadic_primary_two = get_triadics_from_rgba(raw_primary_color)
    
    primary_complement = get_rgba_complement(raw_primary_color)
    
    figure = go.Figure(
        [
            go.Scatter(x=x, y=lowest_data, name="Min", marker={"color": triadic_primary_one}, line={"dash": "dash"}),
            go.Scatter(x=x, y=avg_data, name="Average", marker={"color": triadic_primary_two}, line={"dash": "dash"}),
            go.Scatter(x=x, y=highest_data, name="Max", marker={"color": primary_complement}, line={"dash": "dash"}),
            go.Scatter(x=x, y=team_data, name=team_name, marker={"color": primary_color}),
        ],
        layout={
            "paper_bgcolor": "rgba(0, 0, 0, 0)", # invisible paper background
            "plot_bgcolor": secondary_color,
            "legend_font_color": secondary_text_color,
            "legend_bgcolor": secondary_color,
            "yaxis": {"showgrid": False, "fixedrange": True, "color": "white"},
            "xaxis": {"showgrid": False, "fixedrange": True, "showticklabels": False},
        }
    )

    # update all scatter traces at once
    figure.update_traces(mode="lines",hovertemplate = "%{y}")
    
    figure.update_layout(
        hovermode="y unified", # display hover text when hovering anywhere on line - not just on a point
        legend={
            "orientation": "h",
            "xanchor": "left",
            "x": 0.1,
            "yanchor": "bottom",
            "y": 1.1
        },
        yaxis_title=stat,
    ) 
    
    return dls.DualRing(
        dcc.Graph(
            figure=figure,
            config={'displayModeBar': False},
            id="single-season-rankings-graph"
        ),
    )
    

def get_single_season_games_y_values(df:object, team_name:str, stat:str):
    """
    Calculate and return cumulative sum y-value graph pairs for league min, max, avg, and team data of given stat for each game.

    Args:
        df (DataFrame): League data for each game.
        stat (str): Specific stat to plot.

    Returns:
        tuple: team stat data, league low data, league average data, league max data.
    """    
    # calculate cumulative of stat for each successive game
    game_df = df.copy()
    team_sum = game_df[game_df["Team"] == team_name][stat].cumsum().values
    game_df["sums"] = game_df.groupby("Team")[stat].cumsum()
    lowest_data = game_df.groupby("Game")["sums"].min().values
    avg_data = game_df.groupby("Game")["sums"].mean().values
    highest_data = game_df.groupby("Game")["sums"].max().values
    highest_data[np.argmax(highest_data):] = np.max(highest_data)
    
    return team_sum, lowest_data, avg_data, highest_data


def get_single_season_games_plot(df:object, team_name:str, stat:str):
    """
    Return a team specific themed dcc.Graph of league game data for a given stat.

    Args:
        df (DataFrame): League game specific data.
        team_name (str): Team name to get data from and style graph colors.
        stat (str): Specific stat to plot.

    Returns:
        dcc.Graph: Team color themed graph of team data, league min, league max, and league average.
    """
    sums, lowest_data, avg_data, highest_data = get_single_season_games_y_values(df, team_name, stat)
    
    x = pd.unique(df["Game"])
    
    primary_color = get_colors(team_name, "primary")
    secondary_color = get_colors(team_name, "secondary")
    secondary_text_color = get_colors(team_name, "secondary_text")
    
    raw_primary_color = TEAM_COLORS[team_name]["primary"]
    triadic_primary_one, triadic_primary_two = get_triadics_from_rgba(raw_primary_color)
    
    primary_complement = get_rgba_complement(raw_primary_color)
    
    figure = go.Figure(
        [
            go.Scatter(x=x, y=lowest_data, name="Min", marker={"color": triadic_primary_one}, line={"dash": "dash"}),
            go.Scatter(x=x, y=avg_data, name="Average", marker={"color": triadic_primary_two}, line={"dash": "dash"}),
            go.Scatter(x=x, y=highest_data, name="Max", marker={"color": primary_complement}, line={"dash": "dash"}),
            go.Scatter(x=x, y=sums, name=team_name, marker={"color": primary_color}),
        ],
        layout={
            "paper_bgcolor": "rgba(0, 0, 0, 0)", # invisible paper background
            "plot_bgcolor": secondary_color,
            "legend_font_color": secondary_text_color,
            "legend_bgcolor": secondary_color,
            "yaxis": {"showgrid": False, "fixedrange": True, "color": "white"},
            "xaxis": {"showgrid": False, "fixedrange": True, "color": "white"},
        }
    )

    figure.update_traces(mode="lines", hovertemplate = "%{y}")
    # hover bg color not coloring to plot bg color? Re-set it back to same color as plot
    figure.update_layout(
        hovermode="x unified",
        hoverlabel={"bgcolor": secondary_color, "font_color": secondary_text_color},
        legend={
            "orientation": "h",
            "xanchor": "left",
            "x": 0.1,
            "yanchor": "bottom",
            "y": 1.1
        },
        xaxis_title="Game #",
        yaxis_title=stat,
    )
    
    return dls.DualRing(
        dcc.Graph(
            figure=figure,
            config={'displayModeBar': False},
            id="single-season-game-graph"
        ),
    )


def layout(team=None):
    if team is None:
        return html.Div()

    CURRENT_SEASON = asyncio.run(query_team_stats("season/current_season"))["season"]

    team_response = get_response(build_team_query_url(endpoint="season/team/", team_name=reverse_slugify(team)))
    if team_response[0] != 200:
        return team_404_layout(team_response[0], team)
    team_df = create_formatted_df(team_response[1], index="id", sort_by="Season", ascending=False)
    
    current_season_df = team_df[team_df["Year"] == int(str(CURRENT_SEASON)[:4])]
    
    games_response = get_response(build_team_query_url(endpoint="games/results/season", season=CURRENT_SEASON))
    if games_response[0] != 200:
        return team_404_layout(games_response[0], team)
    games_df = create_formatted_df(games_response[1], index="id", sort_by="Game", ascending=True)

    primary_color = get_colors(reverse_slugify(team), "primary")
    primary_color_soft = TEAM_COLORS[reverse_slugify(team)]["primary"][:-1] + (0.5, )
    secondary_color = get_colors(reverse_slugify(team), "secondary")
    secondary_color_soft = TEAM_COLORS[reverse_slugify(team)]["secondary"][:-1] + (0.5, )
    secondary_color_softer = TEAM_COLORS[reverse_slugify(team)]["secondary"][:-1] + (0.9, )
    
    excluded = ["gp", "game", "rank", "logo", "conference", "division", "city", "state"]
    team_cols = [i for i in current_season_df.columns if "team" not in i.lower() and "season" not in i.lower() and not any([j in i.lower() for j in excluded])]
    game_cols = [i for i in games_df.columns if "team" not in i.lower() and "season" not in i.lower() and not any([j in i.lower() for j in excluded])]    

    return html.Div(
        [
            # dcc.Store(data=current_season_df.to_json(), id="team-stats-df"),
            # dcc.Store(data=games_df.to_json(), id="game-data-df"),
            dcc.Store(data=team, id="team-name"),
            
            get_team_card(team_df.iloc[0]),
            html.Div(get_season_summary(team_df.iloc[0], layout_id=1), id="current-season-summary"),
            dls.DualRing(
                get_agGrid_layout(
                    team_df, 
                    "Team", 
                    "team-stats-grid", 
                    className="ag-theme-alpine team-grid",
                    style={
                        "padding": 50,
                        "height": 500,
                        "--team-text-color-primary": get_colors(reverse_slugify(team), "primary_text"),
                        "--team-text-color-secondary": get_colors(reverse_slugify(team), "secondary_text"),
                        "--team-color-primary": f"rgba{primary_color_soft}",
                        "--team-color-secondary-soft": f"rgba{secondary_color_soft}",
                        "--team-color-secondary-softer": f"rgba{secondary_color_softer}",
                    },
                    dashGridOptions={"pagination": True, "paginationPageSize": 15},
                ),
            ),
            html.Div(style={"borderBottom": 1, "borderBottomStyle": "solid", "width": 500, "color": "white", "margin": "auto", "paddingTop": 25}),
            html.H3("Single Season Stats", style={"color": "white", "display": "flex", "justifyContent": "center", "paddingTop": 25, "paddingBottom": 25}),
            html.Div(
                [
                    html.Div("Season:", style={"color": "white", "paddingRight": "2%"}),
                    get_single_season_dropdown(reverse_slugify(team), options=pd.unique(team_df[team_df["Team"] == reverse_slugify(team)]["Year"]), id="single-season-season-dropdown"),
                ],
                style={"display": "flex", "justifyContent": "center"}
            ),
            dls.DualRing(html.Div(get_season_summary(team_df.iloc[0], layout_id=2), id="selected-season-summary", style={"marginTop": "2%"})),  
            html.Div(
                [
                    html.Div(
                        [
                            html.H5("Game Stat:", style={"color": "white", "paddingTop": "2%", "minWidth": 200}),
                            get_single_season_dropdown(reverse_slugify(team), options=game_cols, id="single-season-games-stat-dropdown"),
                        ],
                        style={"display": "flex", "alignItems": "center", "paddingLeft": "3%"}
                    ),
                    html.Div(
                        [
                            html.H5("Season Stat:", style={"color": "white", "paddingTop": "2%", "minWidth": 200}),
                            get_single_season_dropdown(reverse_slugify(team), options=team_cols, id="single-season-season-stat-dropdown"),
                        ],
                        style={"display": "flex", "alignItems": "center", "paddingLeft": "10%"}
                    ),
                ],
                # style={"display": "flex", "paddingLeft": "20%", "paddingTop": "5%"}
                style={"display": "flex", "justifyContent": "space-evenly", "paddingTop": "5%"}
            ),
            html.Div(
                [
                    get_single_season_games_plot(games_df[games_df["Season"] == CURRENT_SEASON], reverse_slugify(team), "G"),
                    get_single_season_rankings_plot(current_season_df, reverse_slugify(team), "W"),
                ],
                style={"display": "flex", "justifyContent": "space-evenly"}
            ),
            html.Div(style={"minHeight": 700})
        ],
        style={"backgroundImage": f"linear-gradient(to bottom right, {primary_color}, {secondary_color})"}
    )


@callback(
    Output("selected-season-summary", "children"),
    Input("single-season-season-dropdown", "value"),
    State("team-name", "data"),
    prevent_initial_call=True
)
def update_selected_season_summary(year, team_name):
    season = int(f"{year}{year + 1}")
    team_response = get_response(build_team_query_url(endpoint="season/team/", season=season, team_name=reverse_slugify(team_name)))
    team_df = create_formatted_df(team_response[1], index="id")
    return get_season_summary(team_df.iloc[0], layout_id=2)


@callback(
    Output("single-season-game-graph", "figure"),
    Input("single-season-games-stat-dropdown", "value"),
    Input("single-season-season-dropdown", "value"),
    State("team-name", "data"),
    prevent_initial_call=True
)
def update_game_fig(game_stat, year, team_name):
    season = int(f"{year}{year + 1}")
    games_response = get_response(build_team_query_url(endpoint="games/results/season", season=season))
    game_df = create_formatted_df(games_response[1], index="id", sort_by="Game", ascending=True)
    
    # patch to only update specific parts of figure instead of re-drawing the entire figure
    game_fig_patch = Patch()
    game_team_data, lowest_game_data, avg_game_data, highest_game_data = get_single_season_games_y_values(game_df, reverse_slugify(team_name), game_stat)
    game_fig_patch["data"][0]["x"] = pd.unique(game_df["Game"])
    game_fig_patch["data"][0]["y"] = lowest_game_data
    game_fig_patch["data"][1]["x"] = pd.unique(game_df["Game"])
    game_fig_patch["data"][1]["y"] = avg_game_data
    game_fig_patch["data"][2]["x"] = pd.unique(game_df["Game"])
    game_fig_patch["data"][2]["y"] = highest_game_data
    game_fig_patch["data"][3]["x"] = pd.unique(game_df["Game"])
    game_fig_patch["data"][3]["y"] = game_team_data
    
    game_fig_patch["layout"]["yaxis"]["title"]["text"] = game_stat
    
    return game_fig_patch


@callback(
    Output("single-season-rankings-graph", "figure"),
    Input("single-season-season-stat-dropdown", "value"),
    Input("single-season-season-dropdown", "value"),
    State("team-name", "data"),
    prevent_initial_call=True
)
def update_season_fig(season_stat, year, team_name):
    season = f"{year}{year + 1}"
    team_response = get_response(build_team_query_url(endpoint="season/team/", season=season))
    team_df = create_formatted_df(team_response[1], index="id")
    
    season_fig_patch = Patch()
    season_team_data, lowest_season_data, avg_season_data, highest_season_data = get_single_season_ranks_y_values(team_df, reverse_slugify(team_name), season_stat)
    season_fig_patch["data"][0]["y"] = lowest_season_data
    season_fig_patch["data"][1]["y"] = avg_season_data
    season_fig_patch["data"][2]["y"] = highest_season_data
    season_fig_patch["data"][3]["y"] = season_team_data
    
    return season_fig_patch