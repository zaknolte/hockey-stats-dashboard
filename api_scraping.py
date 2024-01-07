import aiohttp
import asyncio
import datetime
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup


def translate_text(text):
    text_map = {
        'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
        'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
        'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
        'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
        'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
        'Ñ': 'N', 'ñ': 'n',
        'Ç': 'C', 'ç': 'c',
        '§': 'S',  '³': '3', '²': '2', '¹': '1'
    }
    try:
        translate = str.maketrans(text_map)
        return text.translate(translate)
    except AttributeError:
        return text


def parse_data(data, keys, default_value):
    try:
        for key in keys:
            data = data[key]
        return data
    except (KeyError, IndexError, TypeError):
        return default_value


def get_per_game_data(stat, games):
    try:
        return stat / games
    except (TypeError, ZeroDivisionError):
        return None
    

def percent_to_total(percentage, total):
    try:
        return round(percentage * total)
    except TypeError:
        return None
    

def get_percentage(stat1, stat2, to_decimal=True):
    try:
        percent = stat1 / stat2
        if to_decimal:
            percent = percent / 100
        return percent
    except (TypeError, ZeroDivisionError):
        return None


def get_team_ids(by="name"):
    url = "https://api.nhle.com/stats/rest/en/team"
    team_data = asyncio.run(query_api(url))["data"]
    if by == "name":
        ids = {translate_text(i["fullName"]): i["id"] for i in team_data}
    elif by == "abbrv":
        ids = {translate_text(i["triCode"]): i["id"] for i in team_data}
    else:
        ids = {i["id"]: translate_text(i["fullName"]) for i in team_data}
    return dict(sorted(ids.items()))
        
        
async def query_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()

    return data


def get_team_data():
    print("Gathering team data...")
    out_data = []
    try:
        url = "https://records.nhl.com/site/api/franchise?include=teams.id&include=teams.fullName&include=teams.logos&include=teams.conference.name&include=teams.division.name&include=teams.arenaName&include=teams.arenaStateProvince&include=teams.arenaCity"
        all_teams = asyncio.run(query_api(url))["data"]
        for franchise in all_teams:
            firt_season = parse_data(franchise, ["firstSeasonId"], None)
            final_season = parse_data(franchise, ["lastSeasonId"], None)
            franchise_id = parse_data(franchise, ["id"], None)
            for team in franchise["teams"]:
                out_data.append(
                    {
                        "model": "teamstats.team",
                        "fields": {
                            "team_id": parse_data(team, ['id'], None),
                            "franchise_id": franchise_id,
                            "name": translate_text(parse_data(team, ["fullName"], None)),
                            "logo": parse_data(team, ["logos", -1, "url"], ""),
                            "conference": parse_data(team, ["conference", "name"], ""),
                            "division": parse_data(team, ["division", "name"], ""),
                            "start_season": firt_season,
                            "final_season": final_season,
                            "city": translate_text(parse_data(team, ["arenaCity"], None)),
                            "state": translate_text(parse_data(team, ["arenaStateProvince"], None)),
                            "venue": translate_text(parse_data(team, ["arenaName"], None)),
                        }
                    }
                )
        print("Team data complete!")
    except Exception as e:
        print(f"Error while scraping data: {e}!")
        print("Partial data being returned...")
    finally:
        return out_data


def get_season_data():
    print("Gathering season data...")
    out_data = []
    try:
        url = "https://api.nhle.com/stats/rest/en/season"
        season_data = sorted(asyncio.run(query_api(url))["data"], key=lambda x: x["seasonOrdinal"])
        for data in season_data:
            out_data.append(
                {
                    "model": "seasonstats.regularseason",
                    "fields": {
                        "year": parse_data(data, ["id"], None),
                        "start_date": datetime.datetime.strptime(data["startDate"], "%Y-%m-%dT%H:%M:%S").date().strftime("%Y-%m-%d"),
                        "end_date": datetime.datetime.strptime(data["regularSeasonEndDate"], "%Y-%m-%dT%H:%M:%S").date().strftime("%Y-%m-%d"),
                        "games_scheduled": parse_data(data, ["numberOfGames"], None),
                        "total_games_played": parse_data(data, ["totalRegularSeasonGames"], None)
                    }
                }
            )
            out_data.append(
                {
                    "model": "seasonstats.playoffseason",
                    "fields": {
                        "year": parse_data(data, ["id"], None),
                        "start_date": datetime.datetime.strptime(data["regularSeasonEndDate"], "%Y-%m-%dT%H:%M:%S").date().strftime("%Y-%m-%d"),
                        "end_date": datetime.datetime.strptime(data["endDate"], "%Y-%m-%dT%H:%M:%S").date().strftime("%Y-%m-%d"),
                        "total_games_played": parse_data(data, ["totalPlayoffGames"], None)
                    }
                }
            )
        print("Season data complete!")
    except Exception as e:
        print(f"Error while scraping data: {e}!")
        print("Partial data being returned...")
    finally:
        return out_data


def get_team_season_data():
    print("Gathering team season data...")
    out_data = []
    team_ids = get_team_ids(by="id")
    try:
        for team in team_ids:
            season_url = f"https://records.nhl.com/site/api/franchise-season-results?cayenneExp=teamId={team}"
            season_data = sorted(asyncio.run(query_api(season_url))["data"], key=lambda x: x["seasonId"])
            
            pp_url = f"https://api.nhle.com/stats/rest/en/team/powerplay?cayenneExp=teamId={team}"
            pp_data = sorted(asyncio.run(query_api(pp_url))["data"], key=lambda x: x["seasonId"])
            
            pk_url = f"https://api.nhle.com/stats/rest/en/team/penaltykill?cayenneExp=teamId={team}"
            pk_data = sorted(asyncio.run(query_api(pk_url))["data"], key=lambda x: x["seasonId"])
            
            penalties_url = f"https://api.nhle.com/stats/rest/en/team/penalties?cayenneExp=teamId={team}"
            penalties_data = sorted(asyncio.run(query_api(penalties_url))["data"], key=lambda x: x["seasonId"])
            
            shots_url = f"https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=teamId={team}"
            shots_data = sorted(asyncio.run(query_api(shots_url))["data"], key=lambda x: x["seasonId"])
            
            faceoff_url = f"https://api.nhle.com/stats/rest/en/team/faceoffpercentages?cayenneExp=teamId={team}"
            faceoff_data = sorted(asyncio.run(query_api(faceoff_url))["data"], key=lambda x: x["seasonId"])
            
            for data in season_data:
                print(f"Gathering team data for {data['teamId']} {data['seasonId']} season...")
                
                goals_pp = None
                goals_against_pp = None
                pp_chances = None
                pp_percent = None
                goals_sh = None
                goals_against_sh = None
                pk_percent = None
                penalty_minutes = None
                penalties = None
                shots = None
                shots_per_game = None
                shots_against = None
                shots_against_per_game = None
                shot_percent = None
                save_percent = None
                faceoffs_taken = None
                faceoff_percent = None
                faceoffs_won = None
                faceoffs_lost = None
                
                # can't filter api by season for data :( have to loop through to match season id
                for pp in pp_data:                
                    if pp["seasonId"] == data["seasonId"]:
                        goals_pp = parse_data(pp, ["powerPlayGoalsFor"], None)
                        goals_against_pp = parse_data(pp, ["shGoalsAgainst"], None)
                        pp_chances = parse_data(pp, ["ppOpportunities"], None)
                        pp_percent = parse_data(pp, ["powerPlayPct"], None)
                        break
                
                for pk in pk_data:
                    if pk["seasonId"] == data["seasonId"]:
                        goals_sh = parse_data(pk, ["shGoalsFor"], None)
                        goals_against_sh = parse_data(pk, ["ppGoalsAgainst"], None)
                        pk_percent = parse_data(pk, ["penaltyKillPct"], None)
                        break
                        
                for penalty in penalties_data:
                    if penalty["seasonId"] == data["seasonId"]:
                        penalty_minutes = parse_data(penalty, ["penaltyMinutes"], None)
                        penalties = parse_data(penalty, ["penalties"], None)
                        break
                        
                for shot in shots_data:
                    if shot["seasonId"] == data["seasonId"]:
                        # can't seem to find total data - only per game data
                        # calculate season total from per game data * games played
                        shots = percent_to_total(parse_data(shot, ["shotsForPerGame"], None), parse_data(shot, ["gamesPlayed"], None))
                        shots_per_game = parse_data(shot, ["shotsForPerGame"], None)
                        shots_against = percent_to_total(parse_data(shot, ["shotsAgainstPerGame"], None), parse_data(shot, ["gamesPlayed"], None))
                        shots_against_per_game = parse_data(shot, ["shotsAgainstPerGame"], None)
                        shot_percent = get_percentage(parse_data(data, ["goals"], None), shots)
                        save_percent = get_percentage(parse_data(data, ["goalsAgainst"], None), shots_against)
                        break
                    
                for faceoff in faceoff_data:
                    if faceoff["seasonId"] == data["seasonId"]:
                        faceoffs_taken = parse_data(faceoff, ["totalFaceoffs"], None)
                        faceoff_percent = parse_data(faceoff, ["faceoffWinPct"], None)
                        faceoffs_won = percent_to_total(faceoff_percent, faceoffs_taken)
                        if faceoff_percent is not None:
                            faceoffs_lost = percent_to_total(1 - faceoff_percent, faceoffs_taken)
                        else:
                            faceoffs_lost = None
                        break
                        
                if data["gameTypeId"] == 2:
                    out_data.append(
                        {
                            "model": "seasonstats.teamregularseason",
                            "pk": data["id"],
                            "fields": {
                                "team": parse_data(data, ["teamId"], None),
                                "season": parse_data(data, ["seasonId"], None),
                                "games_played": parse_data(data, ["gamesPlayed"], None),
                                "wins": parse_data(data, ["wins"], None),
                                "home_wins": parse_data(data, ["homeWins"], None),
                                "away_wins": parse_data(data, ["roadWins"], None),
                                "losses": parse_data(data, ["losses"], None),
                                "home_losses": parse_data(data, ["homeLosses"], None),
                                "away_losses": parse_data(data, ["roadLosses"], None),
                                "overtime_losses": parse_data(data, ["overtimeLosses"], None),
                                "home_overtime_losses": parse_data(data, ["homeOvertimeLosses"], None),
                                "away_overtime_losses": parse_data(data, ["roadOvertimeLosses"], None),
                                "points": parse_data(data, ["points"], None),
                                "goals": parse_data(data, ["goals"], None),
                                "goals_per_game": get_per_game_data(parse_data(data, ["goals"], None), parse_data(data, ["gamesPlayed"], None)),
                                "goals_against": parse_data(data, ["goalsAgainst"], None),
                                "goals_against_per_game": get_per_game_data(parse_data(data, ["goalsAgainst"], None), parse_data(data, ["gamesPlayed"], None)),
                                "goals_pp": goals_pp,
                                "goals_against_pp": goals_against_pp,
                                "goals_sh": goals_sh,
                                "goals_against_sh": goals_against_sh,
                                "pp_chances": pp_chances,
                                "penalty_minutes": penalty_minutes,
                                "penalties_taken": penalties,
                                "pp_percent": pp_percent,
                                "pk_percent": pk_percent,
                                "shots": shots,
                                "shots_per_game": shots_per_game,
                                "shots_against": shots_against,
                                "shots_against_per_game": shots_against_per_game,
                                "shot_percent": shot_percent,
                                "faceoffs_taken": faceoffs_taken,
                                "faceoffs_won": faceoffs_won,
                                "faceoffs_lost": faceoffs_lost,
                                "faceoff_percent": faceoff_percent,
                                "save_percent": save_percent,
                            }
                        }
                    )
                elif data["gameTypeId"] == 3:
                    out_data.append(
                        {
                            "model": "seasonstats.teamplayoffseason",
                            "pk": data["id"],
                            "fields": {
                                "team": parse_data(data, ["teamId"], None),
                                "season": parse_data(data, ["seasonId"], None),
                                "games_played": parse_data(data, ["gamesPlayed"], None),
                                "wins": parse_data(data, ["wins"], None),
                                "home_wins": parse_data(data, ["homeWins"], None),
                                "away_wins": parse_data(data, ["roadWins"], None),
                                "losses": parse_data(data, ["losses"], None),
                                "home_losses": parse_data(data, ["homeLosses"], None),
                                "away_losses": parse_data(data, ["roadLosses"], None),
                                "overtime_losses": parse_data(data, ["overtimeLosses"], None),
                                "home_overtime_losses": parse_data(data, ["homeOvertimeLosses"], None),
                                "away_overtime_losses": parse_data(data, ["roadOvertimeLosses"], None),
                                "points": parse_data(data, ["points"], None),
                                "goals": parse_data(data, ["goals"], None),
                                "goals_per_game": get_per_game_data(parse_data(data, ["goals"], None), parse_data(data, ["gamesPlayed"], None)),
                                "goals_against": parse_data(data, ["goalsAgainst"], None),
                                "goals_against_per_game": get_per_game_data(parse_data(data, ["goalsAgainst"], None), parse_data(data, ["gamesPlayed"], None)),
                                "goals_pp": None,
                                "goals_against_pp": None,
                                "goals_sh": None,
                                "goals_against_sh": None,
                                "pp_chances": None,
                                "penalty_minutes": None,
                                "penalties_taken": None,
                                "pp_percent": None,
                                "pk_percent": None,
                                "shots": None,
                                "shots_per_game": None,
                                "shots_against": None,
                                "shots_against_per_game": None,
                                "shot_percent": None,
                                "faceoffs_taken": None,
                                "faceoffs_won": None,
                                "faceoffs_lost": None,
                                "faceoff_percent": None,
                                "save_percent": None,
                            }
                        }
                )
        print("Team season data complete!")
    except Exception as e:
        print(f"Error while scraping data: {e}!")
        print("Partial data being returned...")
    finally:
        return out_data


def get_player_data():    
    def resolve_position(position_type, handed):
        positions = {
            "C": 1,
            "RW": 2,
            "LW": 3,
            "RD": 4,
            "LD": 5,
            "D": 6,
            "G": 7
        }
        if position_type == "R" or position_type == "L":
            position_type += "W"
            
        if handed is None:
            return [positions[position_type]]
        
        if position_type == "D":
            # nhl api doesn't seem to classify RD or LD
            # assume the side they play and fix later
            defense_handed = {"R": "L", "L": "R"}
            position_type = defense_handed[handed] + "D"
            
        return [positions[position_type]]
    
    def get_out_data(bios_data):
        return {
            "model": "playerstats.player",
            "pk": bios_data["playerId"],
            "fields": {
                "first_name": bios_data["firstName"]["default"],
                "last_name": bios_data["lastName"]["default"],
                "full_name": bios_data["firstName"]["default"] + " " + bios_data["lastName"]["default"],
                "team": parse_data(bios_data, ["currentTeamId"], None),
                "picture": parse_data(bios_data, ["headshot"], None),
                "position": resolve_position(parse_data(bios_data, ["position"], None), parse_data(bios_data, ["shootsCatches"], None)),
                "jersey_number": parse_data(bios_data, ["sweaterNumber"], None),
                "birthday": parse_data(bios_data, ["birthDate"], None),
                "birth_city": parse_data(bios_data, ["birthCity", "default"], None),
                "birth_state": parse_data(bios_data, ["birthStateProvince", "default"], None),
                "birth_country": parse_data(bios_data, ["birthCountry"], None),
                "height_inches": parse_data(bios_data, ["heightInInches"], None),
                "weight": parse_data(bios_data, ["weightInPounds"], None),
                "is_active": parse_data(bios_data, ["isActive"], False),
                "is_rookie": False if parse_data(bios_data, ["careerTotals", "regularSeason", "gamesPlayed"], 0) > 25 else True, # TODO find api endpoint for this
                "handed": parse_data(bios_data, ["shootsCatches"], None),
            }
        }
    
    def try_append_data(player):
        try:
            # see if player data has already been seen and added
            _ = player_dict[player["playerId"]]
        except KeyError:
            # add player data if new player
            player_dict[player["playerId"]] = True
            bios_url = f"https://api-web.nhle.com/v1/player/{player['playerId']}/landing"
            bios_data = asyncio.run(query_api(bios_url))

            out_data.append(get_out_data(bios_data))
            
    print("Gathering player data...")
    print("WARNING! This may take several hours...")
    out_data = []
    player_dict = {}
    try:
        season_url = "https://api.nhle.com/stats/rest/en/season?&sort=id"
        seasons = asyncio.run(query_api(season_url))["data"]
        
        for season in seasons[::-1]:
            year = str(season["id"])[:4]
            game_code = "02"
            print(f"Gathering player data from {year}...")
            # roster api seems to be missing a few players
            # doesn't seem to contain players that might only play 1 or 2 games a season
            # unfortunately query each game instead to ensure collecting players
            
            # 32 teams = 16 pairs * 82 games = 1312 games
            for i in range(1, 1325):
                game_num = str(i).zfill(4)
                boxscore_url = f"https://api-web.nhle.com/v1/gamecenter/{year}{game_code}{game_num}/boxscore"
                boxscore_data = asyncio.run(query_api(boxscore_url))
                
                if boxscore_data is not None:
                    for skater_type in parse_data(boxscore_data, ["boxscore", "playerByGameStats", "homeTeam"], []):
                        for player in parse_data(boxscore_data, ["boxscore", "playerByGameStats", "homeTeam", skater_type], []):
                            try_append_data(player)
                    
                    for skater_type in parse_data(boxscore_data, ["boxscore", "playerByGameStats", "awayTeam"], []):
                        for player in parse_data(boxscore_data, ["boxscore", "playerByGameStats", "awayTeam", skater_type], []):
                            try_append_data(player)
            
        print("Player data complete!")
    except Exception as e:
        print(f"Error while scraping data: {e}.")
        print("Partial data being returned...")
    finally:
        return out_data


def get_playerstats_data():
    print("Gathering playerstats data...")
    print("WARNING! This may take several hours...")
    out_data = []
    team_ids = get_team_ids(by="abbrv")
    try:
        season_url = "https://api.nhle.com/stats/rest/en/season?&sort=id"
        seasons = asyncio.run(query_api(season_url))["data"]
        
        for season in seasons[::-1]:
            for team in team_ids:
                year = season["id"]
                roster_url = f"https://api-web.nhle.com/v1/club-stats/{team}/{year}/2"
                roster_data = asyncio.run(query_api(roster_url))
                
                if roster_data is not None:
                    print(f"Gathering playerstats data from {team} {year}...")
                    for player in roster_data["skaters"]:
                        pp_url = f"https://api.nhle.com/stats/rest/en/skater/powerplay?cayenneExp=playerId={player['playerId']}"
                        pp_data = asyncio.run(query_api(pp_url))["data"]
                        
                        pk_url = f"https://api.nhle.com/stats/rest/en/skater/penaltykill?cayenneExp=playerId={player['playerId']}"
                        pk_data = asyncio.run(query_api(pk_url))["data"]
                        
                        penalties_url = f"https://api.nhle.com/stats/rest/en/skater/penalties?cayenneExp=playerId={player['playerId']}"
                        penalties_data = asyncio.run(query_api(penalties_url))["data"]
                        
                        realtime_url = f"https://api.nhle.com/stats/rest/en/skater/realtime?cayenneExp=playerId={player['playerId']}"
                        realtime_data = asyncio.run(query_api(realtime_url))["data"]
                        
                        faceoff_url = f"https://api.nhle.com/stats/rest/en/skater/faceoffwins?cayenneExp=playerId={player['playerId']}"
                        faceoff_data = asyncio.run(query_api(faceoff_url))["data"]
                        
                        assists_pp = None
                        toi_seconds_pp = None
                        assists_sh = None
                        toi_seconds_sh = None
                        penalties = None
                        hits = None
                        faceoffs_taken = None
                        faceoffs_won = None
                        faceoffs_lost = None
                        
                        # can't filter api by season for data :( have to loop through to match season id
                        for pp in pp_data:                
                            if pp["seasonId"] == year:
                                assists_pp = parse_data(pp, ["ppAssists"], None)
                                toi_seconds_pp = parse_data(pp, ["ppTimeOnIce"], None)
                                break
                        
                        for pk in pk_data:
                            if pk["seasonId"] == year:
                                assists_sh = parse_data(pk, ["shAssists"], None)
                                toi_seconds_sh = parse_data(pk, ["shTimeOnIce"], None)
                                break
                                
                        for penalty in penalties_data:
                            if penalty["seasonId"] == year:
                                penalties = parse_data(penalty, ["penalties"], None)
                                break
                                
                        for real in realtime_data:
                            if real["seasonId"] == year:
                                hits = parse_data(real, ["hits"], None)
                                giveaways = parse_data(real, ["giveaways"], None)
                                takeaways = parse_data(real, ["takeaways"], None)
                                blocked_shots = parse_data(real, ["blockedShots"], None)
                                break
                            
                        for faceoff in faceoff_data:
                            if faceoff["seasonId"] == year:
                                faceoffs_taken = parse_data(faceoff, ["totalFaceoffs"], None)
                                faceoffs_won = parse_data(faceoff, ["totalFaceoffWins"], None)
                                faceoffs_lost = parse_data(faceoff, ["totalFaceoffLosses"], None)
                                break
                    
                        out_data.append(
                            {
                                "model": "seasonstats.playerregularseason",
                                "pk": int(f"{player['playerId']}{year}"),
                                "fields": {
                                    "player": player["playerId"],
                                    "team": team_ids[team],
                                    "season": year,
                                    "goals": parse_data(player, ["goals"], None),
                                    "assists": parse_data(player, ["assists"], None),
                                    "points": parse_data(player, ["points"], None),
                                    "time_on_ice_seconds": percent_to_total(parse_data(player, ["goals"], None), parse_data(player, ["gamesPlayed"], None)),
                                    "games_played": parse_data(player, ["gamesPlayed"], None),
                                    "goals_pp": parse_data(player, ["powerPlayGoals"], None),
                                    "goals_sh": parse_data(player, ["shorthandedGoals"], None),
                                    "assists_pp": assists_pp,
                                    "assists_sh": assists_sh,
                                    "time_on_ice_seconds_pp": toi_seconds_pp,
                                    "time_on_ice_seconds_sh": toi_seconds_sh,
                                    "shots": parse_data(player, ["shots"], None),
                                    "hits": hits,
                                    "penalty_minutes": parse_data(player, ["penaltyMinutes"], None),
                                    "penalties_taken": penalties,
                                    "penalty_seconds_served": penalties * 2, # TODO find api data for this or calculate from games
                                    "faceoffs_taken": faceoffs_taken,
                                    "faceoffs_won": faceoffs_won,
                                    "faceoffs_lost": faceoffs_lost,
                                    "faceoff_percent": parse_data(player, ["faceoffWinPctg"], None),
                                    "giveaways": giveaways,
                                    "takeaways": takeaways,
                                    "blocked_shots": blocked_shots,
                                    "plus_minus": parse_data(player, ["plusMinus"], None),
                                }
                            }
                        )
                        
                    for player in roster_data["goalies"]:
                        skater_diff_url = f"https://api.nhle.com/stats/rest/en/goalie/savesByStrength?cayenneExp=playerId={player['playerId']}"
                        skater_diff_data = faceoff_data = asyncio.run(query_api(skater_diff_url))["data"]
                        
                        shots_against_pp = None
                        saves_pp = None
                        shots_against_sh = None
                        saves_sh = None
                        
                        for data in skater_diff_data:
                            if data["seasonId"] == year:
                                shots_against_pp = parse_data(data, ["shShotsAgainst"], None)
                                saves_pp = parse_data(data, ["shSaves"], None)
                                shots_against_sh = parse_data(data, ["ppShotsAgainst"], None)
                                saves_sh = parse_data(data, ["ppSaves"], None)
                                break
                            
                        out_data.append(
                            {
                                "model": "seasonstats.goalieregularseason",
                                "pk": int(f"{player['playerId']}{year}"),
                                "fields": {
                                    "player": player["playerId"],
                                    "team": team_ids[team],
                                    "season": year,
                                    "goals": parse_data(player, ["goals"], None),
                                    "assists": parse_data(player, ["assists"], None),
                                    "points": parse_data(player, ["points"], None),
                                    "goals_against": parse_data(player, ["goalsAgainst"], None),
                                    "goals_against_average": parse_data(player, ["goalsAgainstAverage"], None),
                                    "shutouts": parse_data(player, ["shutouts"], None),
                                    "time_on_ice_seconds": parse_data(player, ["timeOnIce"], None),
                                    "games_played": parse_data(player, ["gamesPlayed"], None),
                                    "shots_against": parse_data(player, ["shotsAgainst"], None),
                                    "shots_against_pp": shots_against_pp,
                                    "shots_against_sh": shots_against_sh,
                                    "saves": parse_data(player, ["saves"], None),
                                    "saves_pp": saves_pp,
                                    "saves_sh": saves_sh,
                                    "save_percent": parse_data(player, ["savePercentage"], None),
                                    "wins": parse_data(player, ["wins"], None),
                                    "losses": parse_data(player, ["losses"], None),
                                }
                            }
                        )
                
        print("Playerstats data complete!")
    except Exception as e:
        print(f"Error while scraping data: {e}.")
        print("Partial data being returned...")
    finally:
        return out_data


def get_game_data():
    print("Gathering game data...")
    print("WARNING! This may take several hours...")
    out_data = []
    try:
        season_url = "https://api.nhle.com/stats/rest/en/season?&sort=id"
        seasons = asyncio.run(query_api(season_url))["data"]
        
        for season in seasons[::-1]:
            year = str(season["id"])[:4]
            game_code = "02"
            # can't find api endpoint that has all game data - only html scoresheets
            # seasons before 2007 have a different boxscore format or don't exist
            if season["id"] < 20072008:
                break
            else:
                print(f"Gathering game data from {year}...")
                # 32 teams = 16 pairs * 82 games = 1312 games
                for i in range(1, 1325):
                    game_num = str(i).zfill(4)
                    boxscore_url = f"https://api-web.nhle.com/v1/gamecenter/{year}{game_code}{game_num}/boxscore"
                    boxscore_data = asyncio.run(query_api(boxscore_url))

                    home_players = []
                    away_players = []
                    if boxscore_data is not None:
                        game_date = datetime.datetime.strptime(boxscore_data["gameDate"], "%Y-%m-%d")
                        # don't grab data from future games
                        if game_date.date() < datetime.date.today():
                            try:
                                for skater_type in parse_data(boxscore_data, ["boxscore", "playerByGameStats", "homeTeam"], None):
                                    if skater_type:
                                        skaters = parse_data(boxscore_data, ["boxscore", "playerByGameStats", "homeTeam", skater_type], None)
                                        home_players.extend([parse_data(skater, ["playerId"], None) for skater in skaters])
                                        
                                for skater_type in parse_data(boxscore_data, ["boxscore", "playerByGameStats", "awayTeam"], None):
                                    if skater_type:
                                        skaters = parse_data(boxscore_data, ["boxscore", "playerByGameStats", "awayTeam", skater_type], None)
                                        away_players.extend([parse_data(skater, ["playerId"], None) for skater in skaters])
                            except TypeError:
                                pass
                                        
                            out_data.append(
                                {
                                    "model": "gamestats.regulargame",
                                    "pk": boxscore_data["id"],
                                    "fields": {
                                        "players": home_players + away_players or None,
                                        "home_team": parse_data(boxscore_data, ["homeTeam", "id"], None),
                                        "away_team": parse_data(boxscore_data, ["awayTeam", "id"], None),
                                        "season": season["id"],
                                        "game_date": parse_data(boxscore_data, ["gameDate"], None),
                                        "game_start_time": parse_data(boxscore_data, ["startTimeUTC"], None),
                                    }
                                }
                            )
        print("Game data complete!")
    except Exception as e:
        print(f"Error while scraping data: {e}.")
        print("Partial data being returned...")
    finally:
        return out_data

def get_team_game_data():
    def data_to_int(data):
        try:
            return int(data)
        except ValueError:
            return 0
    print("Gathering team game data...")
    print("WARNING! This may take several hours...")
    out_data = []
    team_ids = get_team_ids(by="name")
    try:
        season_url = "https://api.nhle.com/stats/rest/en/season?&sort=id"
        seasons = asyncio.run(query_api(season_url))["data"]
        
        for season in seasons[::-1]:
            year = str(season["id"])[:4]
            game_code = "02"
            # can't find api endpoint that has all game data - only html scoresheets
            # seasons before 2007 have a different scoresheet format or don't exist
            if season["id"] < 20072008:
                break
            else:
                print(f"Gathering team game data from {year}...")
                # 32 teams = 16 pairs * 82 games = 1312 games
                for i in range(1, 1325):
                    try:
                        game_num = str(i).zfill(4)

                        r = requests.get(f"https://www.nhl.com/scores/htmlreports/{season['id']}/ES{game_code}{game_num}.HTM").text

                        soup = BeautifulSoup(r, 'html.parser')

                        game_nums = soup.find_all(style="font-size: 10px;font-weight:bold")
                        home_game_info = game_nums[-1].text.split("Game")
                        home_team = translate_text(home_game_info[0].title())
                        home_team_id = team_ids[home_team]
                        home_team_pk = int(f"{year}{home_team_id}{game_code}{game_num}")
                        home_game_num = data_to_int(home_game_info[1].split(" ")[1])
                        
                        away_game_info = game_nums[0].text.split("Game")
                        away_team = translate_text(away_game_info[0].title())
                        away_team_id = team_ids[away_team]
                        away_team_pk = int(f"{year}{away_team_id}{game_code}{game_num}")
                        away_game_num = data_to_int(away_game_info[1].split(" ")[1])

                        table_rows = soup.find_all("tr", class_="oddColor")
                            
                        home_goals = data_to_int(table_rows[2].text.split("\n")[4].split("-")[0])
                        home_pp_goals = data_to_int(table_rows[2].text.split("\n")[2].split("-")[0])
                        home_sh_goals = data_to_int(table_rows[2].text.split("\n")[3].split("-")[0])
                        home_shots = data_to_int(table_rows[2].text.split("\n")[4].split("-")[-1])

                        away_goals = data_to_int(table_rows[0].text.split("\n")[4].split("-")[0])
                        away_pp_goals = data_to_int(table_rows[0].text.split("\n")[2].split("-")[0])
                        away_sh_goals = data_to_int(table_rows[0].text.split("\n")[3].split("-")[0])
                        away_shots = data_to_int(table_rows[0].text.split("\n")[4].split("-")[-1])

                        totals = soup.find_all(string="TEAM TOTALS")

                        home_totals = totals[-1].parent.parent.find_all("td")
                        home_penalties = data_to_int(home_totals[5].text)
                        home_penalty_minutes = data_to_int(home_totals[6].text) * 60
                        home_hits = data_to_int(home_totals[-7].text)
                        home_giveaways = data_to_int(home_totals[-6].text)
                        home_takeaways = data_to_int(home_totals[-5].text)
                        home_blocked_shots = data_to_int(home_totals[-4].text)
                        home_faceoffs_won = data_to_int(home_totals[-3].text)
                        home_faceoffs_lost = data_to_int(home_totals[-2].text)
                        home_faceoffs_taken = home_faceoffs_won + home_faceoffs_lost
                        home_faceoffs_lost = data_to_int(home_totals[-2].text)
                        try:
                            home_faceoffs_percent = home_faceoffs_won / home_faceoffs_taken
                        except ZeroDivisionError:
                            home_faceoffs_percent = 0

                        away_totals = totals[0].parent.parent.find_all("td")
                        away_penalties = data_to_int(away_totals[5].text)
                        away_penalty_minutes = data_to_int(away_totals[6].text) * 60
                        away_hits = data_to_int(away_totals[-7].text)
                        away_giveaways = data_to_int(away_totals[-6].text)
                        away_takeaways = data_to_int(away_totals[-5].text)
                        away_blocked_shots = data_to_int(away_totals[-4].text)
                        away_faceoffs_won = data_to_int(away_totals[-3].text)
                        away_faceoffs_lost = data_to_int(away_totals[-2].text)
                        away_faceoffs_taken = away_faceoffs_won + away_faceoffs_lost
                        away_faceoffs_lost = data_to_int(away_totals[-2].text)
                        try:
                            away_faceoffs_percent = away_faceoffs_won / away_faceoffs_taken
                        except ZeroDivisionError:
                            away_faceoffs_percent = 0
                            
                        # home team data
                        out_data.append(
                            {
                                "model": "gamestats.teamregulargame",
                                "pk": home_team_pk,
                                "fields": {
                                    "team": home_team_id,
                                    "game": int(f"{year}{game_code}{game_num}"),
                                    "game_number": home_game_num,
                                    "goals": home_goals,
                                    "goals_pp": home_pp_goals,
                                    "goals_sh": home_sh_goals,
                                    "goals_against": away_goals,
                                    "goals_against_pp": away_pp_goals,
                                    "goals_against_sh": away_sh_goals,
                                    "shots": home_shots,
                                    "shots_against": away_shots,
                                    "hits": home_hits,
                                    "penalty_minutes": home_penalty_minutes,
                                    "penalties_taken": home_penalties,
                                    "penalty_seconds_served": home_penalty_minutes, # TODO find or calculate this data
                                    "faceoffs_taken": home_faceoffs_taken,
                                    "faceoffs_won": home_faceoffs_won,
                                    "faceoffs_lost": home_faceoffs_lost,
                                    "faceoff_percent": home_faceoffs_percent,
                                    "giveaways": home_giveaways,
                                    "takeaways": home_takeaways,
                                    "blocked_shots": home_blocked_shots
                                }
                            },
                        )
                        # away team data
                        out_data.append(
                            {
                                "model": "gamestats.teamregulargame",
                                "pk": away_team_pk,
                                "fields": {
                                    "team": away_team_id,
                                    "game": int(f"{year}{game_code}{game_num}"),
                                    "game_number": away_game_num,
                                    "goals": away_goals,
                                    "goals_pp": away_pp_goals,
                                    "goals_sh": away_sh_goals,
                                    "goals_against": home_goals,
                                    "goals_against_pp": home_pp_goals,
                                    "goals_against_sh": home_sh_goals,
                                    "shots": away_shots,
                                    "shots_against": home_shots,
                                    "hits": away_hits,
                                    "penalty_minutes": away_penalty_minutes,
                                    "penalties_taken": away_penalties,
                                    "penalty_seconds_served": away_penalty_minutes, # TODO find or calculate this data
                                    "faceoffs_taken": away_faceoffs_taken,
                                    "faceoffs_won": away_faceoffs_won,
                                    "faceoffs_lost": away_faceoffs_lost,
                                    "faceoff_percent": away_faceoffs_percent,
                                    "giveaways": away_giveaways,
                                    "takeaways": away_takeaways,
                                    "blocked_shots": away_blocked_shots
                                }
                            },
                        )
                    except (KeyError, IndexError):
                        pass
        print("Team game data complete!")
    except Exception as e:
        print(f"Error while scraping data: {e}.")
        print("Partial data being returned...")
    finally:
        return out_data

def write_fixture(app_dir, fixture_name, data):
    print(f"Writing {fixture_name} to {app_dir}/fixtures...")
    path = Path(f"backend/{app_dir}") / "fixtures" / fixture_name
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"{fixture_name} complete!")


if __name__ == "__main__":
    write_fixture("teamstats", "teams.json", get_team_data())
    write_fixture("seasonstats", "seasons.json", get_season_data())
    write_fixture("seasonstats", "teamseasons.json", get_team_season_data())
    write_fixture("playerstats", "players.json", get_player_data())
    write_fixture("seasonstats", "playerseasons.json", get_playerstats_data())
    write_fixture("gamestats", "games.json", get_game_data())
    write_fixture("gamestats", "teamgames.json", get_team_game_data())
