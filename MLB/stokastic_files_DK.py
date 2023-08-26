import pandas as pd

def read_data(file_path, columns_to_use, column_renames):
    """Read data from a CSV and rename columns if specified."""
    df = pd.read_csv(file_path, usecols=columns_to_use)
    df.rename(columns=column_renames, inplace=True)
    return df

def merge_dataframes(primary_df, secondary_df, merge_columns, secondary_columns):
    """Merge two dataframes on specified columns."""
    return primary_df.merge(secondary_df[secondary_columns], on=merge_columns, how='left')

def adjust_stddev_for_pitchers(df):
    """Adjust StdDev for pitchers in the given dataframe."""
    mask = df['Pos'] == 'P'
    df.loc[mask, 'StdDev'] = df.loc[mask, 'Fpts'] * 0.35
    return df

def main():
    # Constants
    FILE_PATHS = {
        "projections": './stokastic/MLB DK Projections.csv',
        "ownership": './stokastic/MLB DK Ownership.csv',
        "hitters": './stokastic/DKTopALL.csv',
        "player_ids": './player_ids.csv',
        "top_stacks": './stokastic/MLB DK TopStacks.csv'
    }
    
    COLUMN_RENAMES = {
        "projections": {'Tm':'Team', 'Sal':'Salary'},
        "ownership": {'Ownership %':'Own%'},
        "top_stacks": {'Ownership share':'Own%'}
    }

    # Read and process projections
    projections = read_data(FILE_PATHS["projections"], 
                            ['Name', 'Fpts', 'Tm', 'Pos', 'Ord', 'Sal'], 
                            COLUMN_RENAMES["projections"])
    projections['Pos'] = projections['Pos'].replace({
        'SS/OF': 'OF/SS',
        'C/1B': '1B/C'
    })

    # Read and process ownership
    ownership = read_data(FILE_PATHS["ownership"], 
                          ['Name', 'Ownership %'], 
                          COLUMN_RENAMES["ownership"])
    ownership['Name'] = ownership['Name'].replace({
        'Nate Lowe': 'Nathaniel Lowe',
        'Josh Palacios': 'Joshua Palacios'
    })

    # Merge projections and ownership
    projections = merge_dataframes(projections, ownership, ['Name'], ['Name', 'Own%'])
    
    # Read and process hitters
    hitters = read_data(FILE_PATHS["hitters"], ['Name', 'StdDev'], {})
    hitters = hitters.drop_duplicates(subset='Name', keep='first')

    # Merge projections and hitters for StdDev
    projections = merge_dataframes(projections, hitters, ['Name'], ['Name', 'StdDev'])
    
    # Adjust StdDev for pitchers
    projections = adjust_stddev_for_pitchers(projections)
    projections['Ceiling'] = projections['Fpts'] + projections['StdDev']

    # Read and process player_ids
    player_ids_df = read_data(FILE_PATHS["player_ids"], ['Name', 'Position', 'TeamAbbrev', 'ID'], {"Position": "Pos", "TeamAbbrev": "Team"})
    player_ids_df['Pos'] = player_ids_df['Pos'].replace({'SP': 'P', 'RP':'P'})
    player_ids_df['ID'] = player_ids_df['ID'].astype(str)

    # Merge projections with player_ids
    projections = merge_dataframes(projections, player_ids_df, ['Name', 'Pos', 'Team'], ['Name', 'Pos', 'Team', 'ID'])

    # Read and process top_stacks
    top_stacks = read_data(FILE_PATHS["top_stacks"], ['Team', 'Ownership share'], COLUMN_RENAMES["top_stacks"])

    # Iterate over each row in the DataFrame
    for index, row in projections.iterrows():
        # Check if there are any NaN values or a zero salary in the row
        if row.isnull().any() or row['Salary'] == '0':
            print(f"\nPlayer {row['Name']} details:")
            print(row.to_string())
            action = input("Do you want to drop the row or fix the issues? (drop/fix): ")
            
            if action.lower() == 'drop':
                projections.drop(index, inplace=True)
                print(f"Row for {row['Name']} dropped.")
            elif action.lower() == 'fix':
                for column, value in row.items():
                    # If the value is NaN or it's the 'Salary' column with a value of '0'
                    if pd.isnull(value) or (column == 'Salary' and value == '0'):
                        while True:  # Add this loop to keep prompting the user for valid input
                            new_value = input(f"Enter a new value for {row['Name']}'s {column}: ")
                            
                            # Convert the input to the appropriate data type based on the column name
                            if column in ['Fpts', 'Own%', 'StdDev', 'Ceiling']:
                                try:
                                    new_value = float(new_value)  # Convert to float
                                    break  # Exit the while loop if input is valid
                                except ValueError:
                                    # Handle cases where conversion to float is not possible
                                    print(f"Invalid input for {column}. Please enter a numeric value.")
                            elif column in ['Pos', 'Salary', 'ID']:
                                # For 'Pos', 'Salary', and 'ID' columns, leave it as a string
                                break
                            else:
                                print(f"Unexpected column {column}. Value left unchanged.")
                                break
                        
                        # Update the DataFrame with the new value
                        projections.at[index, column] = new_value

    # Export data to CSV
    EXPORT_PATHS = ['./projections.csv', './boom_bust.csv', './ownership.csv', './team_stacks.csv']
    DATAFRAMES_TO_EXPORT = [projections, projections, projections, top_stacks]
    for df, path in zip(DATAFRAMES_TO_EXPORT, EXPORT_PATHS):
        df.to_csv(path, index=False)
    
    return projections, top_stacks

if __name__ == "__main__":
    projections_global, top_stacks_global = main()
