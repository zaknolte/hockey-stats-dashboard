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
    "team.name": "Team",
    "player.position": "Position",
    "season.year": "Season",
    "season.season_type": "Season Type",
    "goals": "Goals",
    "assists": "Assists",
    "points": "Points",
    "time_on_ice_seconds": "TOI",
    "time_on_ice_seconds_pp": "PP TOI",
    "time_on_ice_seconds_sh": "SH TOI",
    "games_played": "GP",
    "goals_pp": "PP Goals",
    "goals_sh": "SH Goals",
    "assists_pp": "PP Assists",
    "assists_sh": "SH Assists",
    "shots": "Shots",
    "hits": "Hits",
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
    "saves_pp": "PP Saves",
    "saves_sh": "SH Saves",
    "wins": "Wins"    
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
    

def get_ag_grid_columnDefs(grid_type:str):
    """
    Return a list of all columnDef fields to add to existing dag.AgGrid.
 
    Args:
        grid_type (str): Type of grid data to create.
 
    Returns:
        List of dicts of all columnDef field parameters.
    """
    columnDefs = [
        add_default_text_columnDef(rename_data_df_cols["player.full_name"], pinned="left", lockPinned=True, cellRenderer="NameLink"),
        add_default_number_columnDef(rename_data_df_cols["season.year"], center=False, width=None),
        {"field": rename_data_df_cols["season.season_type"]},
        {"field": rename_data_df_cols["player.team.name"]},
        {"field": rename_data_df_cols["player.position"], "cellStyle": {"textAlign": "center"}},
        add_default_number_columnDef(rename_data_df_cols["games_played"], headerTooltip="Games Played"),
    ]
    if grid_type != "G":
        player_defs = [
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
    else:
        player_defs = [
            add_default_number_columnDef(rename_data_df_cols["wins"], headerName=abbreviated_data_df_cols["wins"], headerTooltip="Wins"),
            add_default_number_columnDef(rename_data_df_cols["shots_against"], headerName=abbreviated_data_df_cols["shots_against"], headerTooltip="Shots Against"),
            add_default_number_columnDef(rename_data_df_cols["saves"], headerName=abbreviated_data_df_cols["saves"], headerTooltip="Saves"),
            add_default_number_columnDef(rename_data_df_cols["shots_against_pp"], headerName=abbreviated_data_df_cols["shots_against_pp"], headerTooltip="Shots Against on Powerplay"),
            add_default_number_columnDef(rename_data_df_cols["saves_pp"], headerName=abbreviated_data_df_cols["saves_pp"], headerTooltip="Saves on Powerplay"),
            add_default_number_columnDef(rename_data_df_cols["shots_against_sh"], headerName=abbreviated_data_df_cols["shots_against_sh"], headerTooltip="Shots Against when Shorthanded"),
            add_default_number_columnDef(rename_data_df_cols["saves_sh"], headerName=abbreviated_data_df_cols["saves_sh"], headerTooltip="Saves when Shorthanded"),
        ]
        
    return columnDefs + player_defs