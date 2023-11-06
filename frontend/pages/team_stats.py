import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.graph_objs as go

import aiohttp
import asyncio
import base64
import pandas as pd
import numpy as np

from django.utils.text import slugify
from pathlib import Path
from io import StringIO

from data_values import TEAM_COLORS, TEAM_TEXT_COLOR
from helpers import reverse_slugify, rename_data_df_cols, get_colors


def title(team):
    return team.replace("-", " ").title()


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
        api_url = f"http://127.0.0.1:8000/api/{endpoint}"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


CURRENT_SEASON = asyncio.run(query_team_stats("season/current_season"))["season"]


def query_to_formatted_df(query: str, index=None, sort_by=None, ascending=False):
    """
    Queries backend database for data then formats the returned data into a dataFrame.

    Args:
        query (str): The url endpoint to query including query params.

    Returns:
        obj: Formatted dataFrame of database data.
    """
    df = pd.json_normalize(asyncio.run(query_team_stats(query)))
    
    if index is not None:
        df= df.set_index(index)
        
    df = df.rename(columns=rename_data_df_cols)
    print(df.columns)
    if sort_by is not None:
        df = df.sort_values(sort_by, ascending=ascending)
    
    return df


def build_team_query_url(endpoint, **kwargs):
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
def format_image(image_url):
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
    img_path = "/".join([i for i in DJANGO_ROOT.parts]) + "/images/team-logos/"
    picture_name = image_url.split("/")[-1]

    encoded = base64.b64encode(open(img_path + picture_name, "rb").read())
    return encoded.decode()


def get_team_card(team_data):
    logo = team_data[rename_data_df_cols["team.logo"]][1:].replace("%3A", ":").replace("%20", " ")
    return html.Div(
        dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.CardImg(
                                src="data:image/png;base64,{}".format(format_image(logo)),
                                className="img-fluid rounded-start",
                                style={"maxWidth": 200}
                            ),
                            className="col-md-4",
                        ),
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4(team_data[rename_data_df_cols["team.name"]], className="card-title"),
                                    html.Div(
                                        [
                                            html.B("Conference:", style={"fontWeight": "bold", "paddingRight": 5}),
                                            html.P(team_data[rename_data_df_cols["team.conference"]])
                                        ],
                                        className="card-text",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.B("Division:", style={"fontWeight": "bold", "paddingRight": 5}),
                                            html.P(team_data[rename_data_df_cols["team.division"]])
                                        ],
                                        className="card-text",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.B("Inagural Season:", style={"fontWeight": "bold", "paddingRight": 5}),
                                            html.P(team_data[rename_data_df_cols["team.start_season"]])
                                        ],
                                        className="card-text",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.P(f"{team_data[rename_data_df_cols['team.city']]}, {team_data[rename_data_df_cols['team.state']]}")
                                        ],
                                        className="card-text",
                                    ),
                                ]
                            ),
                            className="col-md-8",
                            style={"paddingLeft": 10, "color": "white"}
                            # style={"paddingLeft": 10, "color": TEAM_TEXT_COLOR[team_data["team"]["name"]][0]}
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


def get_season_summary(team_data, offset, layout_id):
    col_style = {"border": 1, "borderRightStyle": "solid", "display": "flex", "justifyContent": "center"}
    return [
            dbc.Row(
                [
                    dbc.Col("Season", width={"size": 1, "offset": offset}, style=col_style),
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
                    dbc.Col(team_data[rename_data_df_cols["season.year"]], width={"size": 1, "offset": offset}, style=col_style),
                    dbc.Col(team_data[rename_data_df_cols["games_played"]], width=1, style=col_style),
                    dbc.Col(team_data[rename_data_df_cols["wins"]], width=1, style=col_style),
                    dbc.Col(team_data[rename_data_df_cols["losses"]], width=1, style=col_style),
                    # TODO add ROW data to model
                    dbc.Col("??", width=1, style=col_style),
                    dbc.Col(team_data[rename_data_df_cols["overtime_loss"]], width=1, style=col_style),
                    dbc.Col(team_data[rename_data_df_cols["points"]], width=1, style=col_style),
                    dbc.Col(team_data[rename_data_df_cols["rank"]], width=1, style=col_style),
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


def get_single_season_dropdown(df):
    team_name = df[rename_data_df_cols['team.name']].values[0]

    return html.Div(
        dcc.Dropdown(
            options=pd.unique(df[rename_data_df_cols["season.year"]]),
            value=df[rename_data_df_cols["season.year"]].values[0],
            clearable=False,
            searchable=False,
            id="dropdown-team-season",
            className="team-stats",
            style={
                "width": "100px",
                "backgroundColor": get_colors(team_name, "secondary"),
                "--team-text-color-primary": get_colors(team_name, "primary_text"),
                "--team-text-color-secondary": get_colors(team_name, "secondary_text"),
                "--team-color-primary": get_colors(team_name, "primary"),
                "--team-color-secondary": get_colors(team_name, "secondary")
            },
        ),
    )
    

def get_single_season_rankings_plot(df, team_name, season, stat):
    team_data = df[(df[rename_data_df_cols["team.name"]] == reverse_slugify(team_name)) & (df[rename_data_df_cols["season.year"]] == season)][stat]
    lowest_data = df[stat].min()
    avg_data = df[stat].mean()
    highest_data = df[stat].max()
    x = [i for i in range(1, 11)]
    
    primary_color = get_colors(reverse_slugify(team_name), "primary")
    secondary_color = get_colors(reverse_slugify(team_name), "secondary")
    secondary_text_color = get_colors(reverse_slugify(team_name), "secondary_text")
    
    figure = go.Figure(
        [
            go.Scatter(x=x, y=[lowest_data]*len(x), name="Min", marker={"color": "#16FF32", "line": {"color": "#16FF32"}}),
            go.Scatter(x=x, y=[avg_data]*len(x), name="Average", marker={"color": "#0DF9FF", "line": {"color": "#0DF9FF"}}),
            go.Scatter(x=x, y=[highest_data]*len(x), name="Max", marker={"color": "#A777F1", "line": {"color": "#A777F1"}}),
            go.Scatter(x=x, y=[team_data.iloc[0]]*len(x), name=reverse_slugify(team_name), marker={"color": primary_color, "line_color": primary_color}),
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

    figure.update_traces(hoverinfo="name", mode="lines")
    
    return dcc.Graph(
        figure=figure,
        config={'displayModeBar': False},
    )


def layout(team=None):
    if team is None:
        return html.Div()

    season_summary_df = query_to_formatted_df(build_team_query_url(endpoint="season/teams", team="All Teams", season="All Seasons", season_type="Regular Season"), index="id", sort_by=rename_data_df_cols["season.year"])
    team_df = season_summary_df[season_summary_df[rename_data_df_cols["team.name"]] == reverse_slugify(team)]
    games_df = query_to_formatted_df(query="games/results/all", index=None, sort_by=rename_data_df_cols["game_number"], ascending=True)

    primary_color = get_colors(team_df[rename_data_df_cols["team.name"]].values[0], "primary")
    secondary_color = get_colors(team_df[rename_data_df_cols["team.name"]].values[0], "secondary")

    return html.Div(
        [
            dcc.Store(data=season_summary_df.to_json(), id="team-stats-df"),
            dcc.Store(data=team, id="team-name"),
            dcc.Store(data=games_df.to_json(), id="game-data-df"),
            
            get_team_card(team_df.iloc[0]),
            html.Div(get_season_summary(team_df.iloc[0], offset=2, layout_id=1), id="current-season-summary"),
            html.Div(style={"borderBottom": 1, "borderBottomStyle": "solid", "width": 500, "color": "white", "margin": "auto", "paddingTop": 25}),
            html.H3("Single Season Stats", style={"color": "white", "display": "flex", "justifyContent": "center", "paddingTop": 25, "paddingBottom": 25}),
            html.Div(
                [
                    html.Div("Season:", style={"color": "white", "paddingRight": "2%"}),
                    get_single_season_dropdown(team_df),
                    html.Div(
                        get_season_summary(team_df.iloc[0], offset=1, layout_id=2),
                        id="selected-season-summary",
                        style={"width": "100%"}),
                ],
                style={"display": "flex", "paddingLeft": "5%", "alignItems": "center"}
            ),
            get_single_season_rankings_plot(season_summary_df, team, CURRENT_SEASON, rename_data_df_cols["wins"]),
            html.Div(style={"minHeight": 700})
        ],
        style={"backgroundImage": f"linear-gradient(to bottom right, {primary_color}, {secondary_color})"}
    )


@callback(
    Output("selected-season-summary", "children"),
    Input("dropdown-team-season", "value"),
    State("team-stats-df", "data"),
    State("team-name", "data"),
    # prevent_initial_call=True
)
def update_selected_season_summary(season, data, team_name):
    df = pd.read_json(StringIO(data))
    team_df = df[(df[rename_data_df_cols["team.name"]] == reverse_slugify(team_name)) & (df[rename_data_df_cols["season.year"]] == season)]
    return get_season_summary(team_df.iloc[0], offset=1, layout_id=2)


