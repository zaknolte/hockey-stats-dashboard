from dash import html, dcc, callback, Output, Input, no_update
import dash_bootstrap_components as dbc
from dash import html

from django.utils.text import slugify
import aiohttp
import asyncio
import pandas as pd

from data_values import DIVISION_TEAMS


async def query_all_player_names():
    """
    Performs an async query to the backed server to get all player names.

    Returns:
        json response of data.
    """
    async with aiohttp.ClientSession() as session:
        api_url = f"http://127.0.0.1:8000/api/players/all_names"
        async with session.get(api_url) as resp:
            data = await resp.json()

    return data


def get_player_names():
    """
    Queries backend database for data then returns list of player names.

    Returns:
        list: List of all player names in json format.
    """
    return asyncio.run(query_all_player_names())

def get_options_from_names():
    return [
        {
            "label": player["name"],
            "value": player["id"],
        } for player in get_player_names()
    ]


def build_team_col(division, division_teams):
    col = [
        html.Div(division, className="text-center px-3"),
        html.Hr(),
    ]

    for team in division_teams[division]:
        ref = slugify(team)
        col.append(
            dbc.DropdownMenuItem(team, href=f"http://127.0.0.1:8050/teams/{ref}", className="text-center px-3"),
        )
    
    return col


nav = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Players", href="/players")),
        dbc.DropdownMenu(
            children=[
                dbc.Container(
                    [
                        dbc.Row(
                            dbc.Col(build_team_col("Pacific", DIVISION_TEAMS)),
                        ),
                        dbc.Row(
                            dbc.Col(build_team_col("Central", DIVISION_TEAMS)),
                        ),
                        dbc.Row(
                            dbc.Col(build_team_col("Metropolitan", DIVISION_TEAMS)),
                        ),
                        dbc.Row(
                            dbc.Col(build_team_col("Atlantic", DIVISION_TEAMS)),
                        ),
                    ],
                    class_name="d-flex justify-content-between",
                ),
            ],
            nav=True,
            in_navbar=True,
            label="Teams",
            align_end=True,
        ),
        # dbc.NavItem(dbc.NavLink("League", href="/league")),
        dcc.Dropdown(
            placeholder="Search Players...",
            options=get_options_from_names(),
            style={"width": 200, "backgroundColor": "black", "borderColor": "darkgrey", "marginTop": "0.5%"},
            className="player-search",
            id="player-search",
            maxHeight=0,
            ),
        dcc.Location(id="player-routing")
    ],
    brand="Home",
    brand_href="/",
    color="primary",
    dark=True,
    class_name="d-flex justify-content-start",
)


# change the dropdown to mimic a traditional search bar
# hide options until a search is started
@callback(
    Output("player-search", "maxHeight"),
    Input("player-search", "search_value")
)
def show_dropdown(value):
    if value:
        return 500
    return 0

# player dropdown links only work when clicking on the name itself
# add additional dcc.Location routing if selecting player by pressing Enter
# or by selecting the dropdown option row area next to the text
@callback(
    Output("player-routing", "href"),
    Input("player-search", "value")
)
def route_player_page(name):
    if name:
        return f"http://127.0.0.1:8050/player/{name}"
    return no_update