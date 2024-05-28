import dash_ag_grid as dag
import numpy as np
import re

from data_values import TEAM_COLORS

# helper dict to rename data from database to a more readable column header
rename_data_df_cols = {
    "name": "Name",
    "player": "Player",
    "position": "Position",
    "team": "Team",
    "team.name": "Team",
    "goals": "G",
    "assists": "A",
    "points": "P",
    "time_on_ice_seconds": "TOI",
    "games_played": "GP",
    "goals_pp": "PP G",
    "goals_sh": "SH G",
    "assists_pp": "PP A",
    "assists_sh": "SH A",
    "time_on_ice_seconds_pp": "TOI PP",
    "time_on_ice_seconds_sh": "TOI SH",
    "shots": "Shots",
    "hits": "Hits",
    "penalty_minutes": "PIM",
    "penalties_taken": "Penalties",
    "penalty_seconds_served": "PSS",
    "faceoffs_taken": "FO",
    "faceoffs_won": "FO W",
    "faceoffs_lost": "FO L",
    "faceoff_percent": "FO %",
    "giveaways": "Giveaways",
    "takeaways": "Takeaways",
    "blocked_shots": "Blocks",
    "plus_minus": "+/-",
    "season": "Season",
    "year": "Year",
    "full_season": "Full Season",
    "goals_against": "GA",
    "goals_against_average": "GAA",
    "shutouts": "SO",
    "shots_against": "Shots Against",
    "shots_against_pp": "PP Shots Against",
    "shots_against_sh": "SH Shots Against",
    "saves": "Saves",
    "saves_pp": "PP S",
    "saves_sh": "SH S",
    "save_percent": "Save %",
    "wins": "W",
    "losses": "L",
    "overtime_loss": "OTL",
    "overtime_losses": "OTL",
    "home_wins": "Home W",
    "away_wins": "Away W",
    "ties": "T",
    "home_ties": "Home T",
    "away_ties": "Away T",
    "home_losses": "Home L",
    "away_losses": "Away L",
    "home_overtime_losses": "Home OTL",
    "away_overtime_losses": "Away OTL",
    "goals_per_game": "G/G",
    "goals_against_per_game": "GA/G",
    "goals_against_pp": "PP GA",
    "goals_against_sh": "SH GA",
    "pp_chances": "PP Chances",
    "pp_percent": "PP %",
    "pk_percent": "PK %",
    "shots_per_game": "Shots/G",
    "shots_against_per_game": "Shots Against/G",
    "shot_percent": "Shot %",
    "game_number": "Game",
    "game.season": "Season",
}


def get_stat_sorting(stat):    
    ascending_stats = {
        "GA": True,
        "GAA": True,
    }
    
    try:
        return ascending_stats[stat]
    except KeyError:
        return False
    
def get_colors(team_name:str, color="primary"):
    """
    Return a formatted css rgba string for a specific team of type 'color'
    
    Example: get_colors('Arizona Coyotes', 'secondary') -> 'rgba(226, 214, 181, 1)'
 
    Args:
        team_name (str): Team name to get color values for.
        color (str): Specific color to obtain. Ex: 'primary', 'secondary', 'primary_text', etc.
 
    Returns:
        str: String of css rgba color.
    """
    colors = {
        "primary": f"rgba{TEAM_COLORS[team_name]['primary']}",
        "primary_text": f"rgba{TEAM_COLORS[team_name]['primary_text']}",
        "secondary": f"rgba{TEAM_COLORS[team_name]['secondary']}",
        "secondary_text": f"rgba{TEAM_COLORS[team_name]['secondary_text']}",
    }
    
    return colors.get(color, "primary")


def get_triadics_from_rgba(rgba:tuple):
    """
    Return two formatted css rgba strings equal distances on the color wheel from the given 'rgba'.
    
    Example: get_triadics_from_rgba((255, 125, 34, 1)) -> 'rgba(34, 255, 125, 1), rgba(125, 34, 255, 1)'
 
    Args:
        rgba (tuple): Tuple of rgba values to calculate triadics.
 
    Returns:
        tuple[str]: Strings of css rgba colors for (triadic 1, triadic 2).
    """
    first = tuple(np.append(np.roll(rgba[:-1], 1), rgba[-1]))
    second = tuple(np.append(np.roll(first[:-1], 1), first[-1]))
    
    return f"rgba{first}", f"rgba{second}"


def get_rgba_complement(rgba:tuple):
    """
    Return a formatted css rgba string opposite on the color wheel from given 'rgba'.
    
    Example: get_rgba_complement((255, 125, 0, 1)) -> 'rgba(0, 125, 255, 1)'
 
    Args:
        rgba (tuple): Tuple of rgba values to calculate complement.
 
    Returns:
        tuple[str]: Strings of css rgba colors for (triadic 1, triadic 2).
    """
    rgb_complement = [255-i for i in rgba[:-1]]
    rgb_complement.append(rgba[-1])
    
    return f"rgba{tuple(rgb_complement)}"


def stringify_season(season:int):
    """
    Return a string representation of the full league season. If given an int of 2023, will return '2023-2024'
 
    Args:
        season (str): Year that the season begins.
 
    Returns:
        str: String of season range.
    """
    # return f"{season}-{season + 1}"
    return str(season)[:4] + "-" + str(season)[4:]


def slugify(text):
    value = str(value)
    value = (unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii"))
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

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



def cols_to_percent(df, cols):
    for col in cols:
        try:
            df[col] = df[col] * 100
        except KeyError:
            pass
    return df

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
    

def get_agGrid_columnDefs(grid_type:str, add_link=True):
    """
    Return a list of all columnDef fields to add to existing dag.AgGrid.
 
    Args:
        grid_type (str): Type of grid data to create.
 
    Returns:
        List of dicts of all columnDef field parameters.
    """
    base_defs = [
        add_default_number_columnDef("Year", width=None),
        {"field": "Team"},
        {"field": "Position", "cellStyle": {"textAlign": "center"}},
        add_default_number_columnDef("GP", headerTooltip="Games Played"),
    ]
    if add_link:
        base_defs .insert(0, add_default_text_columnDef("PlayerLink", pinned="left", lockPinned=True, cellRenderer="markdown", headerName="Name"))
    if grid_type == "Team":
        column_defs = [
            add_default_number_columnDef("Year", pinned="left", lockPinned=True),
            add_default_text_columnDef("Team"),
            add_default_number_columnDef("GP", headerTooltip="Games Played"),
            add_default_number_columnDef("W", headerTooltip="Wins"),
            add_default_number_columnDef("L", headerTooltip="Losses"),
            add_default_number_columnDef("OTL", headerTooltip="Overtime Losses"),
            add_default_number_columnDef("P", headerTooltip="Points"),
            add_default_number_columnDef("G/G", headerTooltip="GPG"),
            add_default_number_columnDef("GA/G", headerTooltip="Goals Against Per Game"),
            add_default_number_columnDef("PP G", headerTooltip="Powerplay Goals"),
            add_default_number_columnDef("PP GA", headerTooltip="Goals Against on Powerplay"),
            add_default_number_columnDef("SH G", headerTooltip="Shorthanded Goals"),
            add_default_number_columnDef("SH GA", headerTooltip="Goals Against when Shorthanded"),
            add_default_number_columnDef("PP Chances", headerTooltip="Powerplay Chances"),
            add_default_number_columnDef("PIM", headerTooltip="Penalty Minutes"),
            add_default_number_columnDef("Penalties", headerTooltip="Penalties Taken"),
            add_default_number_columnDef("PP %", headerTooltip="Powerplay %"),
            add_default_number_columnDef("PK %", headerTooltip="Penaltykill %"),
            add_default_number_columnDef("Shots", headerTooltip="Shots"),
            add_default_number_columnDef("Shots Against", headerTooltip="Shots Against"),
            add_default_number_columnDef("Shots/G", headerTooltip="Shots Per Game"),
            add_default_number_columnDef("Shots Against/G", headerTooltip="Shots Against Per Game"),
            add_default_number_columnDef("Shot %", headerTooltip="Shooting %"),
            add_default_number_columnDef("FO", headerTooltip="Faceoffs Taken"),
            add_default_number_columnDef("FO W", headerTooltip="Faceoffs Won"),
            add_default_number_columnDef("FO L", headerTooltip="Faceoffs Lost"),
            add_default_number_columnDef("FO %", headerTooltip="Faceoff %"),
            add_default_number_columnDef("Save %", headerTooltip="Save Percent"),            
        ]
    elif grid_type != "G":
        skater_defs = [
            add_default_number_columnDef("G", headerTooltip="Goals"),
            add_default_number_columnDef("A", headerTooltip="Assists"),
            add_default_number_columnDef("P", headerTooltip="Points}"),
            add_default_number_columnDef("+/-", headerTooltip="Plus-Minus"),
            add_default_number_columnDef("PP G", headerTooltip="Powerplay Goals"),
            add_default_number_columnDef("PP A", headerTooltip="Powerplay Assists"),
            add_default_number_columnDef("SH G",  headerTooltip="Shorthanded Goals"),
            add_default_number_columnDef("SH A", headerTooltip="Shorthanded Assists"),
            add_default_number_columnDef("FO %", headerTooltip="Faceoff %"),
            add_default_number_columnDef("Giveaways", headerTooltip="Giveaways", width=None),
            add_default_number_columnDef("Takeaways", headerTooltip="Takeaways", width=None),
            add_default_number_columnDef("Blocks", width=None),
        ]
        column_defs = base_defs + skater_defs
    else:
        goalie_defs = [
            add_default_number_columnDef("W", headerTooltip="Wins"),
            add_default_number_columnDef("L", headerTooltip="Losses"),
            add_default_number_columnDef("Save %"),
            add_default_number_columnDef("GA", headerTooltip="Goals Against"),
            add_default_number_columnDef("GAA", headerTooltip="Goals Against Average"),
            add_default_number_columnDef("SO"),
            add_default_number_columnDef("SA", headerTooltip="Shots Against"),
            add_default_number_columnDef("Saves", headerTooltip="Saves"),
            add_default_number_columnDef("PP SA", headerTooltip="Shots Against on Powerplay"),
            add_default_number_columnDef("PP S", headerTooltip="Saves on Powerplay"),
            add_default_number_columnDef("SH SA", headerTooltip="Shots Against when Shorthanded"),
            add_default_number_columnDef("SH S", headerTooltip="Saves when Shorthanded"),
            add_default_number_columnDef("G", headerTooltip="Goals"),
            add_default_number_columnDef("A", headerTooltip="Assists"),
            add_default_number_columnDef("P", headerTooltip="Points}"),
        ]
        column_defs = base_defs + goalie_defs
        
    return column_defs


def get_agGrid_layout(df:object, grid_type:str, grid_id:str, add_link=True, **kwargs):
    """
    Return stylized ag Grid of filtered data.
    Will default to use ag-theme-alpine theme. Can optionally provide a className kwarg that corresponds to a custom css class.
 
    Args:
        df (obj): dataFrame of filtered data.
        grid_type (str): Group used to select displayed columns.
        grid_id (str): Id of grid component.
 
    Returns:
        obj: ag Grid.
    """
    try:
        className = kwargs.pop("className")
    except KeyError:
        className = "ag-theme-alpine base-grid"
        
    return dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=get_agGrid_columnDefs(grid_type, add_link),
            id=grid_id,
            className=className,
            columnSize="autoSize",
            defaultColDef = {"headerClass": 'center-aligned-header'},
            **kwargs,
        )