import os
import pandas as pd

def main():
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct file paths relative to the script's location
    regions_file = os.path.join(script_dir, '../data/raw/IMF Data regions.csv')
    countries_file = os.path.join(script_dir, '../data/raw/IMF Data countries.csv')
    analytical_groups_file = os.path.join(script_dir, '../data/raw/IMF Data analytical-groups.csv')
    processed_file = os.path.join(script_dir, '../data/processed/IMF Data full.csv')

    # Load the regions dataset from a CSV file
    regions_df = pd.read_csv(regions_file)

    # Load the countries dataset from a CSV file
    countries_df = pd.read_csv(countries_file)

    # Load the analytical groups dataset from a CSV file
    analytical_group_df = pd.read_csv(analytical_groups_file)

    # Drop nulls
    regions_df.dropna(inplace=True)
    countries_df.dropna(inplace=True)

    # Remove the bracketed units from the column names of the countries dataframe
    countries_df.columns = countries_df.columns.str.replace(r' \[\w+\]', '', regex=True)

    # Remove the bracketed units from the column names of the regions dataframe
    regions_df.columns = regions_df.columns.str.replace(r' \[\w+\]', '', regex=True)

    # Remove the 'Series Name' column from the regions dataframe
    regions_df.drop(columns=['Series Name'], inplace=True)
    # Remove the 'Series Name' column from the countries dataframe
    countries_df.drop(columns=['Series Name'], inplace=True)

    # Add a 'Type' column to the regions dataframe and set all values to 'Region'
    regions_df['Type'] = 'Region'
    # Add a 'Type' column to the countries dataframe and set all values to 'Country'
    countries_df['Type'] = 'Country'

    # Drop nulls
    analytical_group_df.dropna(inplace=True)

    # Remove specific columns from the DataFrame that represent years not needed
    analytical_group_df.drop(
        columns=[
            '1980',
            '1981',
            '1982',
            '1983',
            '1984',
            '1985',
            '1986',
            '1987',
            '1988',
            '1989',
            '2024',
            '2025',
            '2026',
            '2027',
            '2028',
            '2029',
        ],
        inplace = True,
    )

    # Rename the 'Real GDP growth (Annual percent change)' column to 'Country Name' in order to match original dataset
    analytical_group_df.rename(columns={'Real GDP growth (Annual percent change)': 'Country Name'}, inplace=True)

    # Add a new column called 'Type' to the DataFrame and set all its values to 'Analytical group'
    analytical_group_df['Type'] = 'Analytical group'
    
    # Combine dataframes
    combined_df = pd.concat([regions_df, countries_df, analytical_group_df], ignore_index=True, axis=0)

    # Save the modified DataFrame to a new CSV file, excluding the index
    combined_df.to_csv(processed_file, index=False)

if __name__ == '__main__':
    main()