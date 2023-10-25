import pandas as pd

# ==== Configuration Section ====

IMPORT_PATHS = {
    "boom_bust": "./NBA DK Boom Bust.csv",
    "projections": "./NBA DK Projections.csv",
    "template": "./Projection_Template_NBA.csv",
}

EXPORT_PATHS = {
    "updated_template": "./updated_template.csv"
}

# Possible column names mapping to standardized names
COLUMNS_MAPPING = {
    "Ownership": ["Ownership%"], 
    "StdDev": ["Std Dev"],
    "FieldPts": ["Field Points"],    
}

REQUIRED_COLUMNS = ["Projection", "Minutes", "Ownership"]
OPTIONAL_COLUMNS = ["StdDev", "FieldPts"]

# Name replacements for known mismatches
NAME_REPLACEMENTS = {
    # 'incorrect_name': 'correct_name'
    'Scotty Pippen': 'Scotty Pippen Jr.',
    # Add more as needed
}


# ==== Functions Definitions ====

def load_data(import_paths):
    return pd.read_csv(import_paths["template"]), pd.read_csv(import_paths["boom_bust"]), pd.read_csv(import_paths["projections"])

def standardize_column_names(df, column_mapping, required, optional):
    for standard_name, possible_names in column_mapping.items():
        
        # Check if standard_name is already in columns
        if standard_name in df.columns:
            continue  # Skip to next iteration if standard_name is already a column
        
        for name in possible_names:
            if name in df.columns:
                df.rename(columns={name: standard_name}, inplace=True)
                break
        else:
            if standard_name in required:
                raise ValueError(f"Required column '{standard_name}' or its alternatives not found.")
            elif standard_name in optional:
                print(f"Optional column '{standard_name}' not found. Defaults will be used.")
    return df

def correct_names(df):
    df['Name'] = df['Name'].replace(NAME_REPLACEMENTS)
    return df

def map_names_and_ids(template, boom_bust, projections):
    template["name_lower"] = template["Name"].str.strip().str.lower()
    boom_bust["name_lower"] = boom_bust["Name"].str.strip().str.lower()
    projections["name_lower"] = projections["Name"].str.strip().str.lower()

    boom_bust["ID"] = boom_bust["name_lower"].map(template.set_index("name_lower")["PlayerId"])
    projections["ID"] = projections["name_lower"].map(template.set_index("name_lower")["PlayerId"])

    mismatched = False  # flag to indicate if there's a mismatch

    # Check for mismatches in boom_bust
    mismatched_rows_bb = boom_bust[boom_bust["ID"].isna()][["Name", "Team"]]
    if not mismatched_rows_bb.empty:
        print("The following players from 'boom_bust' could not be matched:")
        for _, row in mismatched_rows_bb.iterrows():
            print(f"{row['Name']} ({row['Team']})")
        mismatched = True

    # Check for mismatches in projections
    mismatched_rows_proj = projections[projections["ID"].isna()][["Name", "Team"]]
    if not mismatched_rows_proj.empty:
        print("The following players from 'projections' could not be matched:")
        for _, row in mismatched_rows_proj.iterrows():
            print(f"{row['Name']} ({row['Team']})")
        mismatched = True

    return not mismatched  # Return True if there's no mismatch


def map_data_and_export(template, boom_bust, projections, export_path):
    boom_bust.loc[(boom_bust["Ownership"] == 0) | (boom_bust["Ownership"].isna()), "Ownership"] = 0.1

    template["Projection"] = template["PlayerId"].map(boom_bust.set_index("ID")["Projection"])
    template["Minutes"] = template["PlayerId"].map(projections.set_index("ID")["Minutes"])
    template["Ownership"] = template["PlayerId"].map(boom_bust.set_index("ID")["Ownership"])

    for col in OPTIONAL_COLUMNS:
        if col in boom_bust.columns:
            template[col] = template["PlayerId"].map(boom_bust.set_index("ID")[col])
    
    template = template.dropna(subset=["Projection", "Ownership"])
    template = template.drop(columns=["name_lower"])
    template.reset_index(drop=True, inplace=True)
    template.to_csv(export_path, index=False)

    return template

# ==== Main ====

template, boom_bust, projections = load_data(IMPORT_PATHS)

boom_bust = standardize_column_names(boom_bust, COLUMNS_MAPPING, REQUIRED_COLUMNS, OPTIONAL_COLUMNS)

boom_bust = correct_names(boom_bust)
projections = correct_names(projections)

proceed = map_names_and_ids(template, boom_bust, projections)
if proceed:
    template = map_data_and_export(template, boom_bust, projections, EXPORT_PATHS["updated_template"])
else:
    print("Process stopped due to Name mismatches.")
