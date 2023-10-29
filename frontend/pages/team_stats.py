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

from data_values import TEAM_COLORS, TEAM_TEXT_COLOR
from helpers import reverse_slugify


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
        api_url = f"http://127.0.0.1:8000/api/season/{endpoint}"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


def build_team_query_url(team, season, season_type="Regular Season"):
    """
    Builds and returns a query url to query the backend database.
 
    Args:
        season (int): The year of the season start e.g. 2023 for the 2023-2024 season.
        season_type (str): The season type to query. One of 'Pre-Season', 'Regular Season', or 'Playoffs'.
        team (str): A specific team to query or 'All Teams'.
 
    Returns:
        str: The compiled endpoint url string.
    """
    return f"teams?season={season}&season_type={season_type}&team_name={team}"


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
    logo = team_data["team"]["logo"][1:].replace("%3A", ":").replace("%20", " ")
    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src="data:image/png;base64,{}".format(format_image(logo)),
                            className="img-fluid rounded-start",
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(team_data["team"]["name"], className="card-title"),
                                html.Div(
                                    [
                                    html.B("Conference:", style={"fontWeight": "bold", "paddingRight": 5}),
                                    html.P(team_data["team"]["conference"])
                                    ],
                                    className="card-text",
                                    style={"display": "flex"}
                                ),
                                html.Div(
                                    [
                                    html.B("Division:", style={"fontWeight": "bold", "paddingRight": 5}),
                                    html.P(team_data["team"]["division"])
                                    ],
                                    className="card-text",
                                    style={"display": "flex"}
                                ),
                                html.Div(
                                    [
                                    html.B("Inagural Season:", style={"fontWeight": "bold", "paddingRight": 5}),
                                    html.P(team_data["team"]["start_season"])
                                    ],
                                    className="card-text",
                                    style={"display": "flex"}
                                ),
                                html.Div(
                                    [
                                    html.P(f"{team_data['team']['city']}, {team_data['team']['state']}")
                                    ],
                                    className="card-text",
                                ),
                            ]
                        ),
                        className="col-md-8",
                        style={"paddingLeft": 10, "color": TEAM_TEXT_COLOR[team_data["team"]["name"]][0]}
                    ),
                ],
                className="g-0 d-flex align-items-center",
            )
        ],
        className="mb-3 border-0 bg-transparent",
        style={"maxWidth": "540px", "paddingTop": 10},
    )

def layout(team=None):
    if team is None:
        return html.Div()
    
    team_data = asyncio.run(query_team_stats(build_team_query_url(team=reverse_slugify(team), season=2023, season_type="Regular Season")))[0]
    primary_color = TEAM_COLORS[team_data["team"]["name"]][0]
    secondary_color = TEAM_COLORS[team_data["team"]["name"]][1]
    
    return html.Div(
        [
            html.Div(
                [
                    get_team_card(team_data)
                ],
                style={"display": "flex", "justifyContent": "center"}
            ),
        ],
        # style={"backgroundColor": f"rgba{secondary_color}"}
        style={"backgroundImage": f"linear-gradient(to bottom right, rgba{primary_color}, rgba{secondary_color})"}
    )
