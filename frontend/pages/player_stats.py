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

from django.utils.text import slugify
from pathlib import Path
from io import StringIO

from data_values import TEAM_COLORS
from helpers import reverse_slugify, rename_data_df_cols, cols_to_percent, get_colors, get_triadics_from_rgba, get_rgba_complement, get_agGrid_layout, stringify_season


def title(player):
    return f"Hockey Stats | {player.replace('-', ' ').title()}"


dash.register_page(__name__, path_template="/player/<player>", title=title)

async def query_player_stats(endpoint):
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


def query_to_formatted_df(query: str, index=None, sort_by=None, ascending=False):
    """
    Queries backend database for data then formats the returned data into a dataFrame.

    Args:
        query (str): The url endpoint to query including query params.

    Returns:
        obj: Formatted dataFrame of database data.
    """
    df = pd.json_normalize(asyncio.run(query_player_stats(query)))
    
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


def build_player_query_url(endpoint:str, **kwargs):
    """
    Builds and returns a query url to query the backend database.

    Args:
        season (int): The year of the season start e.g. 2023 for the 2023-2024 season.
        season_type (str): The season type to query. One of 'Pre-Season', 'Regular Season', or 'Playoffs'.
        player (str): A specific player to query or 'All players'.

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

def get_player_card(player_data:object):
    """
    Build and return a card of general player information including logo, division, conference, and inagural season.

    Args:
        player_data (DataFrame): DataFrame data of a given player.

    Returns:
        html.Div: Card component of player information.
    """
    logo = player_data["picture"].replace("%3A", ":/").replace("%20", " ")
    
    if any([player_data["birth_city"], player_data["birth_state"], player_data["birth_country"]]):
        place = [player_data["birth_city"], player_data["birth_state"], player_data["birth_country"]]
        place = ", ".join([i for i in place if i is not None])
        born = html.P(place, style={"fontSize": "0.8rem"})
    else:
        born = html.Div()
        
    if player_data["team"] is not None:
        team = html.Div(
                    [
                        html.B("Team:"),
                        html.P(player_data["team"]["name"])
                    ],
                    className="card-text player",
                    style={"display": "flex"}
                )
    else:
        team = html.Div()
        
    return html.Div(
        dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.CardImg(
                                src=format_image(logo),
                                className="img-fluid rounded-start",
                                style={"width": 300}
                            ),
                            className="col-md-5",
                        ),
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4(player_data["full_name"], className="card-title"),
                                    team,
                                    html.Div(
                                        [
                                            html.B("Position:"),
                                            html.P(",".join([i for i in player_data["position"]]))
                                        ],
                                        className="card-text player",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.B("Height:"),
                                            html.P(player_data["height_inches"])
                                        ],
                                        className="card-text player",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.B("Weight:"),
                                            html.P(player_data["weight"])
                                        ],
                                        className="card-text player",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(
                                        [
                                            html.B("Jersey Number:"),
                                            html.P(player_data["jersey_number"])
                                        ],
                                        className="card-text player",
                                        style={"display": "flex"}
                                    ),
                                    html.Div(html.B(player_data["birthday"]), className="card-text player"),
                                    born,
                                ]
                            ),
                            className="col-md-7",
                            style={"paddingLeft": 10}
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
    
    
def layout(player=None):
    if player is None:
        return html.Div()
    
    player_stats = query_to_formatted_df(build_player_query_url(endpoint=f"season/skater/{player}"))
    player_info = asyncio.run(query_player_stats(build_player_query_url(endpoint="players/", player=player)))
    
    return html.Div(
        [
            get_player_card(player_info)
        ]
    )