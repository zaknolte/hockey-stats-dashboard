import dash
from dash import html
import aiohttp
import asyncio

dash.register_page(__name__, path="/players")

async def get_player_stats():

    async with aiohttp.ClientSession() as session:

        api_url = 'http://127.0.0.1:8000/api/players/'
        async with session.get(api_url) as resp:
            data = await resp.json()
    
    return data
    



def layout():
    players = asyncio.run(get_player_stats())
    print(players)
    return html.Div(
    [
        html.H1("player stats go here"),
        html.Div([html.H1(player['first_name']) for player in players])
    ]
)
