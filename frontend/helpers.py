def stringify_season(season):
    return f"{season}-{season + 1}"


rename_data_df_cols = {
    "player.full_name": "Name",
    "player.team_name": "Team",
    "player.position": "Position",
    "season": "Season",
    "season_type": "Season Type",
    "goals": "Goals",
    "assists": "Assists",
    "points": "Points",
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


def add_default_text_columnDef(field):
    return {
            "field": field,
            "filter": "agTextColumnFilter",
            "filterParams": {"buttons": ["reset", "apply"]}
            },
    

def add_default_number_columnDef(field):
    return {
            "field": field,
            "sortable": True,
            "filter": "agNumberColumnFilter",
            "filterParams": {"buttons": ["reset", "apply"]}
            }
    

def get_ag_grid_columnDefs(grid_type):
    if grid_type != "G":
        columnDefs = [
            {
                "field": rename_data_df_cols["player.full_name"],
                "pinned": "left",
                "lockPinned": True,
                "filter": "agTextColumnFilter",
                "filterParams": {"buttons": ["reset", "apply"]}
            },
            {"field": rename_data_df_cols["season"]},
            {"field": rename_data_df_cols["season_type"]},
            {"field": rename_data_df_cols["player.team_name"]},
            {"field": rename_data_df_cols["player.position"]},
            add_default_number_columnDef(rename_data_df_cols["goals"]),
            add_default_number_columnDef(rename_data_df_cols["assists"]),
            add_default_number_columnDef(rename_data_df_cols["points"]),
        ]
    else:
        columnDefs = []
        
    return columnDefs