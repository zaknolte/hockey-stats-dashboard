def stringify_season(season):
    return f"{season}-{season + 1}"


def reverse_slugify(slug):
    return slug.replace("-", " ").title()


rename_data_df_cols = {
    "player.full_name": "Name",
    "player.team.name": "Team",
    "player.position": "Position",
    "season.year": "Season",
    "season.season_type": "Season Type",
    "goals": "G",
    "assists": "A",
    "points": "P",
    "time_on_ice_seconds": "TOI",
    "time_on_ice_seconds_pp": "PP TOI",
    "time_on_ice_seconds_sh": "SH TOI",
    "games_played": "GP",
    "goals_pp": "PP G",
    "goals_sh": "SH G",
    "assists_pp": "PP A",
    "assists_sh": "SH A",
    "shots": "Shots",
    "hits": "Hits",
    "penalty_minutes": "PIM",
    "penalties_taken": "Penalties Taken",
    "penalty_seconds_served": "Penalty Time Served",
    "faceoffs_taken": "F",
    "faceoffs_won": "FW",
    "faceoffs_lost": "FL",
    "faceoff_percent": "F %",
    "giveaways": "Giveaways",
    "takeaways": "Takeaways",
    "blocked_shots": "Blocked Shots",
    "plus_minus": "+/-",
    "shots_against": "SA",
    "shots_against_pp": "PP SA",
    "shots_against_sh": "SH SA",
    "saves": "S",
    "saves_pp": "PP S",
    "saves_sh": "SH S",
    "wins": "W"    
}

base_order_data_df_cols = [
    "Name",
    "Season",
    "Season Type",
    "Team",
    "Position"
]

skater_order_data_df_cols = base_order_data_df_cols + [
    "Goals",
    "Assists",
    "Points"
]

excluded_data_df_cols = [
    "player.id",
    "player.first_name",
    "player.last_name",
    "player.picture"
]


def update_ag_grid_display_cols(df):
    updated_df = df.rename(columns=rename_data_df_cols)
    column_list = base_order_data_df_cols + [i for i in updated_df.columns if i not in excluded_data_df_cols and i not in base_order_data_df_cols]
    return updated_df[column_list]


def add_default_text_columnDef(field, **kwargs):
    columnDef = {
            "field": field,
            "filter": "agTextColumnFilter",
            "filterParams": {"buttons": ["reset", "apply"]}
            }
    columnDef.update(kwargs)
    return columnDef
    

def add_default_number_columnDef(field, **kwargs):
    columnDef = {
            "field": field,
            "sortable": True,
            "filter": "agNumberColumnFilter",
            "filterParams": {"buttons": ["reset", "apply"]}
            }
    columnDef.update(kwargs)
    return columnDef
    

def get_ag_grid_columnDefs(grid_type):
    if grid_type != "G":
        columnDefs = [
            {
                "field": rename_data_df_cols["player.full_name"],
                "pinned": "left",
                "lockPinned": True,
                "filter": "agTextColumnFilter",
                "filterParams": {"buttons": ["reset", "apply"]},
                "cellRenderer": "NameLink",
            },
            add_default_number_columnDef(rename_data_df_cols["season.year"]),
            {"field": rename_data_df_cols["season.season_type"]},
            {"field": rename_data_df_cols["player.team.name"]},
            {"field": rename_data_df_cols["player.position"], "cellStyle":{"textAlign": "center"}},
            add_default_number_columnDef(rename_data_df_cols["games_played"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Games Played"),
            add_default_number_columnDef(rename_data_df_cols["goals"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Goals"),
            add_default_number_columnDef(rename_data_df_cols["assists"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Assists"),
            add_default_number_columnDef(rename_data_df_cols["points"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Points}"),
            add_default_number_columnDef(rename_data_df_cols["plus_minus"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Plus-Minus"),
            add_default_number_columnDef(rename_data_df_cols["goals_pp"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Powerplay Goals"),
            add_default_number_columnDef(rename_data_df_cols["assists_pp"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Powerplay Assists"),
            add_default_number_columnDef(rename_data_df_cols["goals_sh"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Shorthanded Goals"),
            add_default_number_columnDef(rename_data_df_cols["assists_sh"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Shorthanded Assists"),
            add_default_number_columnDef(rename_data_df_cols["faceoff_percent"], flex=500, cellStyle={"textAlign": "center"}, headerTooltip="Faceoff %"),
            add_default_number_columnDef(rename_data_df_cols["giveaways"], flex=500, cellStyle={"textAlign": "center"}),
            add_default_number_columnDef(rename_data_df_cols["takeaways"], flex=500, cellStyle={"textAlign": "center"}),
            add_default_number_columnDef(rename_data_df_cols["blocked_shots"], flex=500, cellStyle={"textAlign": "center"}),
        ]
    else:
        columnDefs = []
        
    return columnDefs