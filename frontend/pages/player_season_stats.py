import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import aiohttp
import asyncio
import base64
import pandas as pd
import numpy as np
from django.utils.text import slugify

from app import DJANGO_ROOT
from helpers import stringify_season

dash.register_page(__name__, path="/players")

# path that stores player images
# /backend/images/
img_path = "/".join([i for i in DJANGO_ROOT.parts])


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
    return html.Div(
        [
            get_leaders_layout(df, "goals"),
            get_leaders_layout(df, "assists"),
            get_leaders_layout(df, "points"),
        ],
        style={"display": "flex", "justifyContent": "space-around"},
    )


def get_leaders_layout(df, stat):
    leaders = df.sort_values(stat, ascending=False).head(10)

    layout = [
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

    return html.Div(
        [
            html.H5(
                stat.title(), style={"display": "flex", "justifyContent": "center"}
            ),
            html.Div(
                [
                    dbc.Container(
                        layout,
                    ),
                ],
            ),
        ],
        style={"width": "15%"},
    )


def layout():
    # get database data
    query = f"?season={CURRENT_SEASON}&season_type=Regular+Season&team_name=All+Teams"
    players_df = pd.json_normalize(asyncio.run(query_player_stats(query))).set_index(
        "id"
    )

    return html.Div(
        [
            get_filter_dropdowns_layout(players_df),
            html.Div(
                [
                    html.H3(
                        ["League Leaders"],
                        style={
                            "display": "flex",
                            "justifyContent": "center",
                            "paddingTop": 50,
                        },
                    )
                ]
            ),
            get_league_leaders_layout(players_df),
        ]
    )
