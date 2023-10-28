def stringify_season(season):
    return f"{season}-{season + 1}"


rename_data_df_cols = {
    "player.full_name": "Name",
    "player.team.name": "Team",
    "player.position": "Position",
    "season.year": "Season",
    "season.season_type": "Season Type",
    "goals": "Goals",
    "assists": "Assists",
    "points": "Points",
    "time_on_ice_seconds": "TOI",
    "time_on_ice_seconds_pp": "PP TOI",
    "time_on_ice_seconds_sh": "SH TOI",
    "games_played": "Games Played",
    "goals_pp": "PP Goals",
    "goals_sh": "SH Goals",
    "assists_pp": "PP Assists",
    "assists_sh": "SH Assists",
    "shots": "Shots",
    "hits": "Hits",
    "penalty_minutes": "PIM",
    "penalties_taken": "Penalties Taken",
    "penalty_seconds_served": "Penalty Time Served",
    "faceoffs_taken": "Faceoffs Taken",
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
            {"field": rename_data_df_cols["player.position"]},
            add_default_number_columnDef(rename_data_df_cols["games_played"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["goals"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["assists"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["points"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["plus_minus"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["goals_pp"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["assists_pp"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["goals_sh"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["assists_sh"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["faceoff_percent"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["giveaways"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["takeaways"], cellStyle={'textAlign': 'center'}),
            add_default_number_columnDef(rename_data_df_cols["blocked_shots"], cellStyle={'textAlign': 'center'}),
        ]
    else:
        columnDefs = []
        
    return columnDefs