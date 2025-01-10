if __name__ == "__main__":
    import pandas as pd

    # Load the regions dataset from a CSV file
    regions_df = pd.read_csv('data/raw/IMF Data regions.csv')
    # Load the countries dataset from a CSV file
    countries_df = pd.read_csv('data/raw/IMF Data countries.csv')

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

    # Concatenate the regions and countries dataframes into a single dataframe
    combined_df = pd.concat([regions_df, countries_df], ignore_index=True, axis=0)
    # Save the combined dataframe to a CSV file
    combined_df.to_csv('data/processed/IMF Data.csv', index=False)