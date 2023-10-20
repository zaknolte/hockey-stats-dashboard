def stringify_season(season):
    return f"{season}-{season + 1}"


ag_grid_cols_rename = {
    "player.full_name": "Name",
    "player.team_name": "Team",
    "player.position": "Position",
    "season": "Season",
    "season_type": "Season Type",
}

ag_grid_cols_reorder = [
    "Name",
    "Season",
    "Season Type",
    "Team",
    "Position"
]

ag_grid_cols_exclude = [
    "player.id",
    "player.first_name",
    "player.last_name",
    "player.picture"
]

def update_ag_grid_display_cols(df):
    updated_df = df.rename(columns=ag_grid_cols_rename)
    column_list = ag_grid_cols_reorder + [i for i in updated_df.columns if i not in ag_grid_cols_exclude and i not in ag_grid_cols_reorder]
    return updated_df[column_list]