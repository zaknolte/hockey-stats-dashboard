import dash_bootstrap_components as dbc
from dash import html

from data_values import DIVISION_TEAMS


def build_team_col(division, division_teams):
    col = [
        html.Div(division, className="text-center px-3"),
        html.Hr(),
    ]

    for team in division_teams[division]:
        ref = team.replace(" ", "-")
        col.append(
            dbc.DropdownMenuItem(team, href=ref, className="text-center px-3"),
        )
    
    return col

pacific_col = build_team_col("Pacific", DIVISION_TEAMS)
central_col = build_team_col("Central", DIVISION_TEAMS)
metro_col = build_team_col("Metropolitan", DIVISION_TEAMS)
atlantic_col = build_team_col("Atlantic", DIVISION_TEAMS)


nav = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Players", href="/players")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(
                    "All Teams", href="/teams", class_name="text-center"
                ),
                html.Hr(),
                dbc.Container(
                    [
                        dbc.Row(
                            dbc.Col(
                                pacific_col,
                                class_name="",
                            ),
                        ),
                        dbc.Row(
                            dbc.Col(
                                central_col,
                                class_name="",
                            ),
                        ),
                        dbc.Row(
                            dbc.Col(
                                metro_col,
                                class_name="",
                            ),
                        ),
                        dbc.Row(
                            dbc.Col(
                                atlantic_col,
                                class_name="",
                            ),
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
