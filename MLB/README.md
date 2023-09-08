# DFS-Tools-Companion/MLB/ README

This directory contains scripts designed to format and prepare data for use with [MLB-DFS-Tools](https://github.com/chanzer0/MLB-DFS-Tools). These utilities are a personal collection, created to complement the main tools. They are based on my own experiences and use-cases and may be beneficial for some users.

## Scripts

1. **stokastic_files_DK.py**: Formats Stokastic projections and related data for DraftKings.
2. **stokastic_files_DK_early.py**: An alternate version of the above, tailored for early games. DKTopALL.csv is not required.

## Pre-requisites

- The scripts expect specific CSV files to be located in the `dk_data/stokastic` sub-directory.
- The scripts are designed with the default location set to the `dk_data` directory. If placed elsewhere, you'll need to adjust the file paths within the script accordingly.

The scripts utilize the following file paths:

```
FILE_PATHS = {
    "projections": './stokastic/MLB DK Projections.csv',
    "ownership": './stokastic/MLB DK Ownership.csv',
    "hitters": './stokastic/DKTopALL.csv',
    "player_ids": './player_ids.csv',
    "top_stacks": './stokastic/MLB DK TopStacks.csv'
}
```

## Output
After processing, the scripts save the formatted data to 'dk_data':
```
EXPORT_PATHS = ['./projections.csv', './boom_bust.csv', './ownership.csv', './team_stacks.csv']
```
These files are ready for use with the main MLB-DFS-Tools.

## Handling Missing Data
If the scripts encounter any missing data (NaN values), they will prompt you with the following:
```
"Do you want to drop the row or fix the issues? (drop/fix): "
```
Depending on your response, the script will either discard the row (player) or pause, allowing for data correction.

## Discord
For questions or further clarifications, join me on the main DFS Tools Discord: https://discord.gg/K9ZACFjEBR

