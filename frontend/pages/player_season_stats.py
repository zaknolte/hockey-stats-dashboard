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


async def get_current_season():
    async with aiohttp.ClientSession() as session:
        api_url = f"http://127.0.0.1:8000/api/players/current_season"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


CURRENT_SEASON = asyncio.run(get_current_season())["season"]
STRING_CURRENT_SEASON = stringify_season(CURRENT_SEASON)


async def get_all_seasons():
    async with aiohttp.ClientSession() as session:
        api_url = f"http://127.0.0.1:8000/api/players/all_seasons"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


ALL_SEASONS = [
    stringify_season(season["season"]) for season in asyncio.run(get_all_seasons())
]


async def get_all_season_types():
    async with aiohttp.ClientSession() as session:
        api_url = f"http://127.0.0.1:8000/api/players/all_season_types"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


ALL_SEASON_TYPES = [k for k in asyncio.run(get_all_season_types())]


# query player season data for every season
async def get_player_stats(
    season=CURRENT_SEASON, season_type="Regular Season", team_name="All Teams"
):
    async with aiohttp.ClientSession() as session:
        api_url = f"http://127.0.0.1:8000/api/players?season={season}&season_type={season_type}&team_name={team_name}"
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
    players_df = pd.json_normalize(asyncio.run(get_player_stats())).set_index("id")

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
