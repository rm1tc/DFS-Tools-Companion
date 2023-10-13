import pandas as pd

# ==== Configuration Section ====

IMPORT_PATHS = {
    "template": "./Projection_Template_NFL.csv",
    "projections": "./projections.csv",
}

EXPORT_PATHS = {
    "updated_template": "./updated_template.csv"
}

# Possible column names mapping to standardized names
COLUMNS_MAPPING = {
    "Name": ["Player"],
    "Projection": ["Projection", "Median", "FD Projection", "FPTS"],
    "Ownership": ["Own%", "Own", "FD Ownership"],
    "StdDev": ["Std Dev", "stddev"],
    "FieldPts": ["Field Points"],
    "ID": ["FDSlateID"]
}
REQUIRED_COLUMNS = ["Projection", "Ownership"]
OPTIONAL_COLUMNS = ["StdDev", "FieldPts"]

# Name replacements for known mismatches
NAME_REPLACEMENTS = {
    'Cardinals': 'Arizona Cardinals',
    'Falcons': 'Atlanta Falcons',
    'Ravens': 'Baltimore Ravens',
    'Bills': 'Buffalo Bills',
    'Panthers': 'Carolina Panthers',
    'Bears': 'Chicago Bears',
    'Bengals': 'Cincinnati Bengals',
    'Browns': 'Cleveland Browns',
    'Cowboys': 'Dallas Cowboys',
    'Broncos': 'Denver Broncos',
    'Lions': 'Detroit Lions',
    'Packers': 'Green Bay Packers',
    'Texans': 'Houston Texans',
    'Colts': 'Indianapolis Colts',
    'Jaguars': 'Jacksonville Jaguars',
    'Chiefs': 'Kansas City Chiefs',
    'Raiders': 'Las Vegas Raiders',
    'Chargers': 'Los Angeles Chargers',
    'Rams': 'Los Angeles Rams',
    'Dolphins': 'Miami Dolphins',
    'Vikings': 'Minnesota Vikings',
    'Patriots': 'New England Patriots',
    'Saints': 'New Orleans Saints',
    'Giants': 'New York Giants',
    'Jets': 'New York Jets',
    'Eagles': 'Philadelphia Eagles',
    'Steelers': 'Pittsburgh Steelers',
    '49ers': 'San Francisco 49ers',
    'Seahawks': 'Seattle Seahawks',
    'Buccaneers': 'Tampa Bay Buccaneers',
    'Titans': 'Tennessee Titans',
    'Commanders': 'Washington Commanders' 
    # Add more as needed
}


# ==== Functions Definitions ====

def load_data(import_paths):
    return pd.read_csv(import_paths["template"]), pd.read_csv(import_paths["projections"])

def standardize_column_names(df, column_mapping, required, optional):
    for standard_name, possible_names in column_mapping.items():
        for name in possible_names:
            if name in df.columns:
                df.rename(columns={name: standard_name}, inplace=True)
                break
        else:
            if standard_name in required:
                raise ValueError(f"Required column '{standard_name}' or its alternatives not found.")
            elif standard_name in optional:
                print(f"Optional column '{standard_name}' not found. Acemind defaults will be used.")
    return df

def correct_names(df):
    df['Name'] = df['Name'].replace(NAME_REPLACEMENTS)
    return df

def map_names_and_ids(template, projections):
    template["name_lower"] = template["Name"].str.strip().str.lower()
    projections["name_lower"] = projections["Name"].str.strip().str.lower()
    
    projections["ID"] = projections["name_lower"].map(template.set_index("name_lower")["PlayerId"])
    
    mismatched_rows = projections[projections["ID"].isna()][["Name", "Team"]]
    if not mismatched_rows.empty:
        print("The following players could not be matched:")
        for _, row in mismatched_rows.iterrows():
            print(f"{row['Name']} ({row['Team']})")
        return False
    return True

def map_data_and_export(template, projections, export_path):
    projections.loc[(projections["Ownership"] == 0) | (projections["Ownership"].isna()), "Ownership"] = 0.1

    template["Projection"] = template["PlayerId"].map(projections.set_index("ID")["Projection"])
    template["Ownership"] = template["PlayerId"].map(projections.set_index("ID")["Ownership"])

    for col in OPTIONAL_COLUMNS:
        if col in projections.columns:
            template[col] = template["PlayerId"].map(projections.set_index("ID")[col])
    
    template = template.dropna(subset=["Projection", "Ownership"])
    template = template.drop(columns=["name_lower"])
    template.reset_index(drop=True, inplace=True)
    template.to_csv(export_path, index=False)

    return template

# ==== Main ====

template, projections = load_data(IMPORT_PATHS)

projections = standardize_column_names(projections, COLUMNS_MAPPING, REQUIRED_COLUMNS, OPTIONAL_COLUMNS)

projections = correct_names(projections)

proceed = map_names_and_ids(template, projections)
if proceed:
    template = map_data_and_export(template, projections, EXPORT_PATHS["updated_template"])
else:
    print("Process stopped due to Name mismatches.")
