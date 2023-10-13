# DFS-Tools-Companion/NFL/ README

This directory contains scripts designed to format and prepare data for use with [AceMind](https://acemind.io/). These utilities are a personal collection, created to complement the main tools. They are based on my own experiences and use-cases and may be beneficial for some users.

## Scripts

1. **acemind_files_DK.py**: Updates the AceMind DraftKings NFL Template [CLASSIC] with the users Stokastic, ETR or PaydirtDFS projections.
2. **acemind_files_FD.py**: Updates the AceMind Fanduel NFL Template [CLASSIC] with the users Stokastic, ETR or PaydirtDFS projections.

## Pre-requisites

- The scripts require the [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) module `pip install pandas` 
- The scripts expect specific CSV files to be located in the same directory. If placed elsewhere, you'll need to adjust the file paths within the script accordingly.
- The scripts have been tested with the listed projections. No column renaming is required. Only the CSV file needs to be renamed. 

The scripts utilize the following file paths:

```
IMPORT_PATHS = {
    "template": "./Projection_Template_NFL.csv",
    "projections": "./projections.csv",
}
```

## Output
After processing, the scripts save the updated template in the same directory:

```
EXPORT_PATHS = {
    "updated_template": "./updated_template.csv"
}
```
The template is ready to use on [AceMind](https://acemind.io/).

## Handling Missing Data
If 'StdDev' or 'FieldPts' columns are not included in the projections.csv the script will ignore these columns and the AceMind defaults will be used.
```
Optional column 'StdDev' not found. Acemind defaults will be used.
Optional column 'FieldPts' not found. Acemind defaults will be used.
```

If the scripts encounter any Name mismatches it will print the mismatched names and stop.
```
The following players could not be matched:
Tony Jones (ARI)
Process stopped due to Name mismatches.
```
The name mismatch will need to be corrected in the projections.csv or the in the NAME_REPLACEMENTS section of the script.
```
# Name replacements for known mismatches
NAME_REPLACEMENTS = {
    # 'incorrect_name': 'correct_name',
    'Tony Jones': 'Tony Jones Jr.', 
    # Add more as needed
}
```

## Discord
For questions or further clarifications, join me on the main DFS Tools Discord: https://discord.gg/K9ZACFjEBR

