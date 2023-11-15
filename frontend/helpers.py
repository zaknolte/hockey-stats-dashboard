import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import numpy as np

from data_values import TEAM_COLORS, TEAM_TEXT_COLOR

def get_colors(team_name, color="primary"):
    colors = {
        "primary": f"rgba{TEAM_COLORS[team_name][0]}",
        "primary_text": f"rgba{TEAM_TEXT_COLOR[team_name][0]}",
        "secondary": f"rgba{TEAM_COLORS[team_name][1]}",
        "secondary_text": f"rgba{TEAM_TEXT_COLOR[team_name][1]}",
    }
    
    return colors.get(color, "primary")


def get_triadics_from_rgba(rgba):
    first = tuple(np.append(np.roll(rgba[:-1], 1), rgba[-1]))
    second = tuple(np.append(np.roll(first[:-1], 1), first[-1]))
    
    return first, second


def get_rgba_complement(rgba):
    rgb_complement = [255-i for i in rgba[:-1]]
    rgb_complement.append(rgba[-1])
    
    return tuple(rgb_complement)


def stringify_season(season:int):
    """
    Return a string representation of the full league season. If given an int of 2023, will return '2023-2024'
 
    Args:
        season (str): Year that the season begins.
 
    Returns:
        str: String of season range.
    """
    return f"{season}-{season + 1}"


def reverse_slugify(slug:str):
    """
    Return an un-slugged string. Will replace all '-' characters with a space and then capitalize each word.
    
    Example: 'arizona-coyotes' -> 'Arizona Coyotes'
 
    Args:
        slug (str): Slug string to be converted.
 
    Returns:
        str: String of season range.
    """
    return slug.replace("-", " ").title()

# helper dict to rename data from database to a more readable column header
rename_data_df_cols = {
    "player.full_name": "Name",
    "player.team.name": "Team",
    "player.position": "Position",
    "season.year": "Season",
    "season.season_type": "Season Type",
    "goals": "Goals",
    "goals_per_game": "Goals/G",
    "goals_against_per_game": "GA/G",
    "assists": "Assists",
    "points": "Points",
    "time_on_ice_seconds": "TOI",
    "time_on_ice_seconds_pp": "PP TOI",
    "time_on_ice_seconds_sh": "SH TOI",
    "games_played": "GP",
    "goals_pp": "PP Goals",
    "goals_against_pp": "PP GA",
    "goals_sh": "SH Goals",
    "goals_against_sh": "SH GA",
    "assists_pp": "PP Assists",
    "assists_sh": "SH Assists",
    "shots": "Shots",
    "shots_pp": "PP Shots",
    "shots_sh": "SH Shots",
    "shots_per_game": "Shots Against/G",
    "shots_against_per_game": "Shots/G",
    "shot_percent": "Shot %",
    "hits": "Hits",
    "pp_chances": "PP Chances",
    "pp_percent": "PP %",
    "pk_percent": "PK %",
    "penalty_minutes": "PIM",
    "penalties_taken": "Penalties Taken",
    "penalty_seconds_served": "Penalty Time Served",
    "faceoffs_taken": "Faceoffs",
    "faceoffs_won": "Faceoffs Won",
    "faceoffs_lost": "Faceoffs Lost",
    "faceoff_percent": "Faceoff %",
    "giveaways": "Giveaways",
    "takeaways": "Takeaways",
    "blocked_shots": "Blocked Shots",
    "plus_minus": "Plus-Minus",
    "shots_against": "Shots Against",
    "shots_against_pp": "PP Shots Against",
    "shots_against_sh": "SH Shots Against",
    "saves": "Saves",
    "save_percent": "Save %",
    "saves_pp": "PP Saves",
    "saves_sh": "SH Saves",
    "wins": "Wins",
    "losses": "Losses",
    "overtime_loss": "OTL",
    "rank": "League Rank",
    "game_number": "Game",
    "game.season": "Season",
    "team.name": "Team",
    "team.logo": "Logo",
    "team.conference": "Conference",
    "team.division": "Division",
    "team.start_season": "Inagural Season",
    "team.city": "City",
    "team.state": "State",
}

# used to abbreviate data from database for more compact readability in tables
# if used in a table, should also add a tooltip for better UX
abbreviated_data_df_cols = {
    "goals": "G",
    "assists": "A",
    "points": "P",
    "goals_pp": "PP G",
    "goals_sh": "SH G",
    "assists_pp": "PP A",
    "assists_sh": "SH A",
    "faceoffs_taken": "F",
    "faceoffs_won": "FW",
    "faceoffs_lost": "FL",
    "faceoff_percent": "F %",
    "plus_minus": "+/-",
    "shots_against": "SA",
    "shots_against_pp": "PP SA",
    "shots_against_sh": "SH SA",
    "saves": "S",
    "saves_pp": "PP S",
    "saves_sh": "SH S",
    "wins": "W"    
}


def add_default_text_columnDef(field:str, **kwargs):
    """
    Add a filterable columnDef field for text data to an existing AG Grid columnDef list.
 
    Args:
        field (str): DataFrame column name to add.
        **kwargs (any): Any acceptable dag.AgGrid columnDefs arguments e.g. 'cellStyle' , 'width', etc..
 
    Returns:
        dict of a single columnDef field parameters.
    """
    columnDef = {
            "field": field,
            "filter": "agTextColumnFilter",
            "filterParams": {"buttons": ["reset", "apply"]}
            }
    columnDef.update(kwargs)
    return columnDef
    

def add_default_number_columnDef(field:str, center=True, **kwargs):
    """
    Add a filterable columnDef field for numeric data to an existing AG Grid columnDef list.
 
    Args:
        field (str): DataFrame column name to add.
        center (bool): Whether to center the data or keep it left-aligned.
        **kwargs (any): Any acceptable dag.AgGrid columnDefs arguments e.g. 'cellStyle' , 'width', etc..
 
    Returns:
        dict of a single columnDef field parameters.
    """
    columnDef = {
            "field": field,
            "sortable": True,
            "filter": "agNumberColumnFilter",
            "filterParams": {"buttons": ["reset", "apply"]},
            "width": 100,
            }
    
    if center:
        columnDef.update({"cellStyle": {"textAlign": "center"}})
    
    columnDef.update(kwargs)
    return columnDef
    

def get_agGrid_columnDefs(grid_type:str):
    """
    Return a list of all columnDef fields to add to existing dag.AgGrid.
 
    Args:
        grid_type (str): Type of grid data to create.
 
    Returns:
        List of dicts of all columnDef field parameters.
    """
    base_defs = [
        add_default_text_columnDef(rename_data_df_cols["player.full_name"], pinned="left", lockPinned=True, cellRenderer="NameLink"),
        add_default_number_columnDef(rename_data_df_cols["season.year"], center=False, width=None),
        {"field": rename_data_df_cols["season.season_type"]},
        {"field": rename_data_df_cols["player.team.name"]},
        {"field": rename_data_df_cols["player.position"], "cellStyle": {"textAlign": "center"}},
        add_default_number_columnDef(rename_data_df_cols["games_played"], headerTooltip="Games Played"),
    ]
    if grid_type == "Team":
        column_defs = [
            add_default_number_columnDef(rename_data_df_cols["season.year"], pinned="left", lockPinned=True),
            add_default_number_columnDef(rename_data_df_cols["games_played"], headerTooltip="Games Played"),
            add_default_number_columnDef(rename_data_df_cols["wins"], headerTooltip="Wins"),
            add_default_number_columnDef(rename_data_df_cols["losses"], headerTooltip="Losses"),
            add_default_number_columnDef(rename_data_df_cols["overtime_loss"], headerTooltip="Overtime Losses"),
            add_default_number_columnDef(rename_data_df_cols["points"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["goals_per_game"], headerTooltip="GPG"),
            add_default_number_columnDef(rename_data_df_cols["goals_against_per_game"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["goals_pp"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["goals_against_pp"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["goals_sh"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["goals_against_sh"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["pp_chances"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["penalty_minutes"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["penalties_taken"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["pp_percent"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["pk_percent"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shots"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shots_against"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shots_per_game"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shots_against_per_game"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shots_pp"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shots_against_pp"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shots_sh"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shots_against_sh"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["shot_percent"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["faceoffs_taken"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["faceoffs_won"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["faceoffs_lost"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["faceoff_percent"], headerTooltip="Points"),
            add_default_number_columnDef(rename_data_df_cols["save_percent"], headerTooltip="Points"),            
        ]
    elif grid_type != "G":
        skater_defs = [
            add_default_number_columnDef(rename_data_df_cols["goals"], headerName=abbreviated_data_df_cols["goals"], headerTooltip="Goals"),
            add_default_number_columnDef(rename_data_df_cols["assists"], headerName=abbreviated_data_df_cols["assists"], headerTooltip="Assists"),
            add_default_number_columnDef(rename_data_df_cols["points"], headerName=abbreviated_data_df_cols["points"], headerTooltip="Points}"),
            add_default_number_columnDef(rename_data_df_cols["plus_minus"], headerName=abbreviated_data_df_cols["plus_minus"], headerTooltip="Plus-Minus"),
            add_default_number_columnDef(rename_data_df_cols["goals_pp"], headerName=abbreviated_data_df_cols["goals_pp"], headerTooltip="Powerplay Goals"),
            add_default_number_columnDef(rename_data_df_cols["assists_pp"], headerName=abbreviated_data_df_cols["assists_pp"], headerTooltip="Powerplay Assists"),
            add_default_number_columnDef(rename_data_df_cols["goals_sh"], headerName=abbreviated_data_df_cols["goals_sh"],  headerTooltip="Shorthanded Goals"),
            add_default_number_columnDef(rename_data_df_cols["assists_sh"], headerName=abbreviated_data_df_cols["assists_sh"], headerTooltip="Shorthanded Assists"),
            add_default_number_columnDef(rename_data_df_cols["faceoff_percent"], headerName=abbreviated_data_df_cols["faceoff_percent"], headerTooltip="Faceoff %"),
            add_default_number_columnDef(rename_data_df_cols["giveaways"], width=None),
            add_default_number_columnDef(rename_data_df_cols["takeaways"], width=None),
            add_default_number_columnDef(rename_data_df_cols["blocked_shots"], width=None),
        ]
        column_defs = base_defs + skater_defs
    else:
        goalie_defs = [
            add_default_number_columnDef(rename_data_df_cols["wins"], headerName=abbreviated_data_df_cols["wins"], headerTooltip="Wins"),
            add_default_number_columnDef(rename_data_df_cols["shots_against"], headerName=abbreviated_data_df_cols["shots_against"], headerTooltip="Shots Against"),
            add_default_number_columnDef(rename_data_df_cols["saves"], headerName=abbreviated_data_df_cols["saves"], headerTooltip="Saves"),
            add_default_number_columnDef(rename_data_df_cols["shots_against_pp"], headerName=abbreviated_data_df_cols["shots_against_pp"], headerTooltip="Shots Against on Powerplay"),
            add_default_number_columnDef(rename_data_df_cols["saves_pp"], headerName=abbreviated_data_df_cols["saves_pp"], headerTooltip="Saves on Powerplay"),
            add_default_number_columnDef(rename_data_df_cols["shots_against_sh"], headerName=abbreviated_data_df_cols["shots_against_sh"], headerTooltip="Shots Against when Shorthanded"),
            add_default_number_columnDef(rename_data_df_cols["saves_sh"], headerName=abbreviated_data_df_cols["saves_sh"], headerTooltip="Saves when Shorthanded"),
        ]
        column_defs = base_defs + goalie_defs
        
    return column_defs


def get_agGrid_layout(df:object, grid_type:str, grid_id, **kwargs):
    """
    Return stylized ag Grid of filtered data.
 
    Args:
        df (obj): dataFrame of filtered data.
        grid_type (str): Group used to select displayed columns.
 
    Returns:
        obj: ag Grid.
    """
    try:
        className = kwargs.pop("className")
    except KeyError:
        className = "ag-theme-alpine base-grid"
        
    return dbc.Spinner(
        dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=get_agGrid_columnDefs(grid_type),
            id=grid_id,
            className=className,
            columnSize="autoSize",
            defaultColDef = {"headerClass": 'center-aligned-header'},
            **kwargs,
        ),
        color="light"
    )
    