import dash
from dash import html, dcc
import aiohttp
import asyncio
import base64
import pandas as pd
import numpy as np

from app import DJANGO_ROOT
from helpers import stringify_season

dash.register_page(__name__, path="/players")

# path that stores player images
# /backend/images/
img_path = "/".join([i for i in DJANGO_ROOT.parts])


# query player season data for every season
async def get_player_stats():
    async with aiohttp.ClientSession() as session:
        api_url = "http://127.0.0.1:8000/api/players/"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


# can't host static images in dash normally outside assets folder
# encode and decode from image url to render image
def format_image(image_url):
    encoded = base64.b64encode(open(img_path + image_url, "rb").read())
    return encoded.decode()


def get_all_teams(df, add_all=True):
    teams_list = pd.unique(df["player.team_name"])
    teams_list.sort()
    if add_all:
        teams_list = np.insert(teams_list, 0, "All Teams")

    return teams_list


def layout():
    # get database data
    players_df = pd.json_normalize(asyncio.run(get_player_stats())).set_index("id")

    # transform data for readability and use
    current_season = stringify_season(players_df["season"].max())
    players_df["season"] = players_df["season"].apply(stringify_season)
    all_teams = get_all_teams(players_df)

    return html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(
                        options=pd.unique(players_df["season"]),
                        value=current_season,
                        style={"width": 500},
                        id="dropdown-button",
                    ),
                    dcc.Dropdown(
                        options=pd.unique(players_df["season_type"]),
                        value="Regular Season",
                        style={"width": 500},
                        id="dropdown-button",
                    ),
                    dcc.Dropdown(
                        options=all_teams,
                        value="All Teams",
                        style={"width": 500},
                        id="dropdown-button",
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-around",
                    "paddingTop": 50,
                },
            )
        ]
    )
