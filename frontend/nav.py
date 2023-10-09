import dash_bootstrap_components as dbc
from dash import html


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
                                [
                                    html.Div("Pacific", className="text-center px-3"),
                                    html.Hr(),
                                    dbc.DropdownMenuItem(
                                        "Page 2", href="#", className="text-center px-3"
                                    ),
                                    dbc.DropdownMenuItem(
                                        "Page 3", href="#", className="text-center px-3"
                                    ),
                                ],
                                class_name="",
                            ),
                        ),
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.Div("Central", className="text-center px-3"),
                                    html.Hr(),
                                    dbc.DropdownMenuItem(
                                        "Page 4", href="#", className="text-center px-3"
                                    ),
                                    dbc.DropdownMenuItem(
                                        "Page 5", href="#", className="text-center px-3"
                                    ),
                                ],
                                class_name="",
                            ),
                        ),
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.Div(
                                        "Metropolitan", className="text-center px-3"
                                    ),
                                    html.Hr(),
                                    dbc.DropdownMenuItem(
                                        "Page 6", href="#", className="text-center px-3"
                                    ),
                                    dbc.DropdownMenuItem(
                                        "Page 7", href="#", className="text-center px-3"
                                    ),
                                ],
                                class_name="",
                            ),
                        ),
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.Div("Atlantic", className="text-center px-3"),
                                    html.Hr(),
                                    dbc.DropdownMenuItem(
                                        "Page 8", href="#", className="text-center px-3"
                                    ),
                                    dbc.DropdownMenuItem(
                                        "Page 9", href="#", className="text-center px-3"
                                    ),
                                ],
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
        ),
    ],
    brand="Home",
    brand_href="/",
    color="primary",
    dark=True,
    class_name="d-flex justify-content-start",
)
