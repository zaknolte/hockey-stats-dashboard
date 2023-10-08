import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from nav import nav


app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
    ],
    use_pages=True,
)

app.layout = html.Div(
    [
        nav(),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
