import os

BACKEND_URL = os.environ.get("BACKEND_URL")
ROOT_URL = os.environ.get("ROOT_URL")

DIVISION_TEAMS = {
    "Pacific": [
        "Anaheim Ducks",
        "Calgary Flames",
        "Edmonton Oilers",
        "Los Angeles Kings",
        "San Jose Sharks",
        "Seattle Kraken",
        "Vancouver Canucks",
        "Vegas Golden Knights",
    ],
    "Central": [
        "Chicago Blackhawks",
        "Colorado Avalanche",
        "Dallas Stars",
        "Minnesota Wild",
        "Nashville Predators",
        "St Louis Blues",
        "Utah Hockey Club",
        "Winnipeg Jets"
    ],
    "Metropolitan": [
        "Carolina Hurricanes",
        "Columbus Blue Jackets",
        "New Jersey Devils",
        "New York Islanders",
        "New York Rangers",
        "Philadelphia Flyers",
        "Pittsburgh Penguins",
        "Washington Capitals"
    ],
    "Atlantic": [
        "Boston Bruins",
        "Buffalo Sabres",
        "Detroit Red Wings",
        "Florida Panthers",
        "Montreal Canadiens",
        "Ottawa Senators",
        "Tampa Bay Lightning",
        "Toronto Maple Leafs"
    ]
}

TEAM_BY_ABBR = {
    "ANA": "Anaheim Ducks",
    "ARI": "Arizona Coyotes",
    "ATL": "Atlanta Thrashers",
    "BOS": "Boston Bruins",
    "BRK": "Brooklyn Americans",
    "BUF": "Buffalo Sabres",
    "CAR": "Carolina Hurricanes",
    "CBJ": "Columbus Blue Jackets",
    "CGS": "California Golden Seals",
    "CGY": "Calgary Flames",
    "CHI": "Chicago Blackhawks",
    "CLE": "Cleveland Barons",
    "CLR": "Colorado Rockies",
    "COL": "Colorado Avalanche",
    "DAL": "Dallas Stars",
    "DCG": "Detroit Cougars",
    "DET": "Detroit Red Wings",
    "DFL": "Detroit Falcons",
    "EDM": "Edmonton Oilers",
    "FLA": "Florida Panthers",
    "HAM": "Hamilton Tigers",
    "HFD": "Hartford Whalers",
    "KCS": "Kansas City Scouts",
    "LAK": "Los Angeles Kings",
    "MIN": "Minnesota Wild",
    "MMR": "Montreal Maroons",
    "MNS": "Minnesota North Stars",
    "MTL": "Montreal Canadiens",
    "MWN": "Montreal Wanderers",
    "NJD": "New Jersey Devils",
    "NSH": "Nashville Predators",
    "NYA": "New York Americans",
    "NYI": "New York Islanders",
    "NYR": "New York Rangers",
    "OAK": "California/Oakland Seals",
    "OTT": "Ottawa Senators",
    "PHI": "Philadelphia Flyers",
    "PHX": "Phoenix Coyotes",
    "PIR": "Pittsburgh Pirates",
    "PIT": "Pittsburgh Penguins",
    "QBD": "Quebec Bulldogs",
    "QUA": "Philadelphia Quakers",
    "QUE": "Quebec Nordiques",
    "SEA": "Seattle Kraken",
    "SEN": "Ottawa Senators",
    "SLE": "St. Louis Eagles",
    "SJS": "San Jose Sharks",
    "STL": "St. Louis Blues",
    "TAN": "Toronto Arenas",
    "TBL": "Tampa Bay Lightning",
    "TOR": "Toronto Maple Leafs",
    "TSP": "Toronto St. Patricks",
    "UTA": "Utah Hockey Club",
    "VAN": "Vancouver Canucks",
    "VGK": "Vegas Golden Knights",
    "WIN": "Winnipeg Jets",
    "WPG": "Winnipeg Jets",
    "WSH": "Washington Capitals",
}

# tuple of rgba values of colors to use for specific teams
TEAM_COLORS = {
    'Anaheim Ducks': {
        "primary": (252, 76, 2, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (185, 151, 91, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Arizona Coyotes': {
        "primary": (140, 38, 51, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (226, 214, 181, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'Atlanta Thrashers': {
        "primary": (40, 30, 66, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (92, 136, 218, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Boston Bruins': {
        "primary": (252, 181, 20, 1),
        "primary_text": (0, 0, 0, 1),
        "secondary": (17, 17, 17, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Buffalo Sabres': {
        "primary": (0, 38, 84, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (252, 181, 20, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'Calgary Flames': {
        "primary": (200, 16, 46, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (241, 190, 72, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'Carolina Hurricanes': {
        "primary": (226, 24, 54, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (35, 31, 32, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Chicago Blackhawks': {
        "primary": (207, 10, 44, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (0, 0, 0, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Colorado Avalanche': {
        "primary": (111, 38, 61, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (35, 91, 146, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Columbus Blue Jackets': {
        "primary": (0, 38, 84, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (206, 17, 38, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Dallas Stars': {
        "primary": (0, 104, 71, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (143, 143, 140, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Detroit Red Wings': {
        "primary": (206, 17, 38, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (255, 255, 255, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'Edmonton Oilers': {
        "primary": (4, 30, 66, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (252, 76, 0, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Florida Panthers': {
        "primary": (4, 30, 66, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (200, 16, 46, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Los Angeles Kings': {
        "primary": (17, 17, 17, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (162, 170, 173, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Minnesota Wild': {
        "primary": (175, 35, 36, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (2, 73, 48, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Montreal Canadiens': {
        "primary": (175, 30, 45, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (25, 33, 104, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Nashville Predators': {
        "primary": (255, 184, 28, 1),
        "primary_text": (0, 0, 0, 1),
        "secondary": (4, 30, 66, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'New Jersey Devils': {
        "primary": (206, 17, 38, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (0, 0, 0, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'New York Islanders': {
        "primary": (0, 83, 155, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (244, 125, 48, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'New York Rangers': {
        "primary": (0, 56, 168, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (206, 17, 38, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Ottawa Senators': {
        "primary": (197, 32, 50, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (194, 145, 44, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Philadelphia Flyers': {
        "primary": (247, 73, 2, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (0, 0, 0, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Pittsburgh Penguins': {
        "primary": (0, 0, 0, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (252, 181, 20, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'San Jose Sharks': {
        "primary": (0, 109, 117, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (0, 0, 0, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Seattle Kraken': {
        "primary": (0, 22, 40, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (153, 217, 217, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'St Louis Blues': {
        "primary": (0, 47, 135, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (252, 181, 20, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'Tampa Bay Lightning': {
        "primary": (0, 40, 104, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (255, 255, 255, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'Toronto Maple Leafs': {
        "primary": (0, 32, 91, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (255, 255, 255, 1),
        "secondary_text": (0, 0, 0, 1),
    },
    'Utah Hockey Club': {
        "primary": (105, 179, 231, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (1, 1, 1, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Vancouver Canucks': {
        "primary": (0, 32, 91, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (4, 28, 44, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Vegas Golden Knights': {
        "primary": (185, 151, 91, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (51, 63, 72, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Washington Capitals': {
        "primary": (4, 30, 66, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (200, 16, 46, 1),
        "secondary_text": (255, 255, 255, 1),
    },
    'Winnipeg Jets': {
        "primary": (4, 30, 66, 1),
        "primary_text": (255, 255, 255, 1),
        "secondary": (0, 76, 151, 1),
        "secondary_text": (255, 255, 255, 1),
    },
}
