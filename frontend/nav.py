import dash_bootstrap_components as dbc
from dash import html

from django.utils.text import slugify

from data_values import DIVISION_TEAMS

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
        dbc.NavItem(dbc.NavLink("League", href="/league")),
    ],
    brand="Home",
    brand_href="/",
    color="primary",
    dark=True,
    class_name="d-flex justify-content-start",
)
