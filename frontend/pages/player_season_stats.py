import dash
from dash import html
import aiohttp
import asyncio
from app import DJANGO_ROOT
import base64

dash.register_page(__name__, path="/players")

# path that stores player images
# /backend/images/
img_path = '/'.join([i for i in DJANGO_ROOT.parts])


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


def layout():
    players = asyncio.run(get_player_stats())
    return html.Div(
        [
            html.H1("player stats go here"),
            html.Div([html.H1(player["first_name"]) for player in players]),
            html.Div([html.Img(src="data:image/png;base64,{}".format(format_image(player["picture"])), width="100px")for player in players]),
        ]
    )
