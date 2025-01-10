import os
import pandas as pd


def load_data(main_file, analytical_groups_file):
    """Loads data from Excel files."""
    try:
        regions_df = pd.read_excel(main_file, sheet_name='Regions')
        countries_df = pd.read_excel(main_file, sheet_name='Country')
        analytical_group_df = pd.read_excel(analytical_groups_file, sheet_name='NGDP_RPCH')
        return regions_df, countries_df, analytical_group_df
    except FileNotFoundError:
        print('Error: One or more files not found. Please check file paths.')
        return None, None, None


def clean_data(regions_df, countries_df, analytical_group_df):
    """Cleans the input dataframes."""
    regions_df.dropna(inplace=True)
    countries_df.dropna(inplace=True)
    analytical_group_df.dropna(inplace=True)

    countries_df.columns = countries_df.columns.str.replace(r' \[\w+\]', '', regex=True)
    regions_df.columns = regions_df.columns.str.replace(r' \[\w+\]', '', regex=True)

    regions_df.drop(columns=['Series Name'], inplace=True)
    countries_df.drop(columns=['Series Name'], inplace=True)

    analytical_group_df.drop(
        columns=[
            1980,
            1981,
            1982,
            1983,
            1984,
            1985,
            1986,
            1987,
            1988,
            1989,
            2024,
            2025,
            2026,
            2027,
            2028,
            2029,
        ],
        inplace=True,
    )
    analytical_group_df.rename(columns={'Real GDP growth (Annual percent change)': 'Country Name'}, inplace=True)

    return regions_df, countries_df, analytical_group_df


def reshape_data(regions_df, countries_df, analytical_group_df):
    """Reshapes the dataframes using melt."""
    regions_df = regions_df.melt(id_vars=['Country Name'], var_name='Year', value_name='GDP_Growth')
    regions_df.rename(columns={'Country Name': 'Region'}, inplace=True)

    countries_df = countries_df.melt(id_vars=['Country Name'], var_name='Year', value_name='GDP_Growth')
    countries_df.rename(columns={'Country Name': 'Country'}, inplace=True)

    analytical_group_df = analytical_group_df.melt(id_vars=['Country Name'], var_name='Year', value_name='GDP_Growth')
    analytical_group_df.rename(columns={'Country Name': 'Analytical Group'}, inplace=True)

    return regions_df, countries_df, analytical_group_df


def create_normalized_tables(countries_df, regions_df, analytical_group_df):
    """Creates normalized tables."""
    # Country Table
    country_table = pd.DataFrame(countries_df['Country'].unique(), columns=['Country'])
    # Region Table
    region_table = pd.DataFrame(regions_df['Region'].unique(), columns=['Region'])
    # Analytical Group Table
    analytical_group_table = pd.DataFrame(
        analytical_group_df['Analytical Group'].unique(), columns=['Analytical Group']
    )

    regions_mapping = {
        "Africa (Region)": [
            "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon",
            "Central African Republic", "Chad", "Comoros", "Congo, Dem. Rep. of the", "Congo, Republic of",
            "Côte d'Ivoire", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia",
            "Gabon", "Gambia, The", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia",
            "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique",
            "Namibia", "Niger", "Nigeria", "Rwanda", "Senegal", "Seychelles", "Sierra Leone", "Somalia",
            "South Africa", "South Sudan, Republic of", "Sudan", "São Tomé and Príncipe", "Tanzania", "Togo",
            "Tunisia", "Uganda", "Zambia", "Zimbabwe"
        ],
        "Asia and Pacific": [
            "Afghanistan", "Armenia", "Australia", "Azerbaijan", "Bangladesh", "Bhutan", "Brunei Darussalam",
            "Cambodia", "China, People's Republic of", "Fiji", "Georgia", "Hong Kong SAR", "India",
            "Indonesia", "Japan", "Kazakhstan", "Kiribati", "Korea, Republic of", "Kyrgyz Republic",
            "Lao P.D.R.", "Macao SAR", "Malaysia", "Maldives", "Marshall Islands", "Micronesia, Fed. States of",
            "Mongolia", "Myanmar", "Nauru", "Nepal", "New Zealand", "Pakistan", "Palau", "Papua New Guinea",
            "Philippines", "Samoa", "Singapore", "Solomon Islands", "Sri Lanka", "Taiwan Province of China",
            "Tajikistan", "Thailand", "Timor-Leste", "Tonga", "Turkmenistan", "Tuvalu", "Türkiye, Republic of",
            "Uzbekistan", "Vanuatu", "Vietnam"
        ],
        "Australia and New Zealand": [
            "Australia", "New Zealand"
        ],
        "Caribbean": [
            "Antigua and Barbuda", "Bahamas, The", "Barbados", "Belize", "Dominica", "Grenada", "Guyana",
            "Haiti", "Jamaica", "Puerto Rico", "Saint Kitts and Nevis", "Saint Lucia",
            "Saint Vincent and the Grenadines", "Suriname", "Trinidad and Tobago"
        ],
        "Central America": [
            "Costa Rica", "Dominican Republic", "El Salvador", "Guatemala", "Honduras", "Nicaragua", "Panama"
        ],
        "Central Asia and the Caucasus": [
            "Afghanistan", "Armenia", "Azerbaijan", "Georgia", "Kazakhstan", "Kyrgyz Republic",
            "Tajikistan", "Turkmenistan", "Türkiye, Republic of", "Uzbekistan"
        ],
        "East Asia": [
            "China, People's Republic of", "Hong Kong SAR", "Japan", "Korea, Republic of", "Macao SAR",
            "Mongolia", "Taiwan Province of China"
        ],
        "Eastern Europe": [
            "Albania", "Belarus", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czech Republic",
            "Estonia", "Hungary", "Kosovo", "Latvia", "Lithuania", "Moldova", "Montenegro",
            "North Macedonia", "Poland", "Romania", "Russian Federation", "Serbia", "Slovak Republic",
            "Slovenia", "Ukraine"
        ],
        "Europe": [
            "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria",
            "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany",
            "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Lithuania",
            "Luxembourg", "Malta", "Moldova", "Montenegro", "Netherlands", "North Macedonia", "Norway",
            "Poland", "Portugal", "Romania", "Russian Federation", "San Marino", "Serbia",
            "Slovak Republic", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom"
        ],
        "Middle East (Region)": [
            "Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Qatar",
            "Saudi Arabia", "Syria", "United Arab Emirates", "West Bank and Gaza", "Yemen"
        ],
        "North Africa": [
            "Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Qatar",
            "Saudi Arabia", "Syria", "United Arab Emirates", "West Bank and Gaza", "Yemen"
        ],
        "North America": [
            "Canada", "Mexico", "United States"
        ],
        "Pacific Islands": [
            "Fiji", "Kiribati", "Marshall Islands", "Micronesia, Fed. States of", "Nauru", "Palau",
            "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
        ],
        "South America": [
            "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru",
            "Uruguay", "Venezuela"
        ],
        "South Asia": [
            "Bangladesh", "Bhutan", "India", "Maldives", "Nepal", "Pakistan", "Sri Lanka"
        ],
        "Southeast Asia": [
            "Brunei Darussalam", "Cambodia", "Indonesia", "Lao P.D.R.", "Malaysia", "Myanmar",
            "Philippines", "Singapore", "Thailand", "Timor-Leste", "Vietnam"
        ],
        "Sub-Saharan Africa (Region)": [
            "Brunei Darussalam", "Cambodia", "Indonesia", "Lao P.D.R.", "Malaysia", "Myanmar",
            "Philippines", "Singapore", "Thailand", "Timor-Leste", "Vietnam"
        ],
        "Western Europe": [
            "Andorra", "Austria", "Belgium", "Cyprus", "Denmark", "Finland", "France", "Germany", "Greece",
            "Iceland", "Ireland", "Italy", "Luxembourg", "Malta", "Netherlands", "Norway", "Portugal",
            "San Marino", "Spain", "Sweden", "Switzerland", "United Kingdom"
        ],
        "Western Hemisphere (Region)": [
            "Antigua and Barbuda", "Argentina", "Bahamas, The", "Barbados", "Belize", "Bolivia", "Brazil",
            "Canada", "Chile", "Colombia", "Costa Rica", "Dominica", "Dominican Republic", "Ecuador",
            "El Salvador", "Grenada", "Guatemala", "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico",
            "Nicaragua", "Panama", "Paraguay", "Peru", "Puerto Rico", "Saint Kitts and Nevis",
            "Saint Lucia", "Saint Vincent and the Grenadines", "Suriname", "Trinidad and Tobago",
            "United States", "Uruguay", "Venezuela"
        ]
    }
    
    analytical_group_mapping = {
        "ASEAN-5": ["Indonesia", "Malaysia", "Philippines", "Singapore", "Thailand"],
        "Advanced economies": [
            "Andorra", "Australia", "Austria", "Belgium", "Canada", "Croatia", "Cyprus", "Czech Republic", "Denmark",
            "Estonia", "Finland", "France", "Germany", "Greece", "Hong Kong SAR", "Iceland", "Ireland", "Israel", "Italy",
            "Japan", "Korea, Republic of", "Latvia", "Lithuania", "Luxembourg", "Macao SAR", "Malta", "Netherlands",
            "New Zealand", "Norway", "Portugal", "Puerto Rico", "San Marino", "Singapore", "Slovak Republic", "Slovenia",
            "Spain", "Sweden", "Switzerland", "Taiwan Province of China", "United Kingdom", "United States"
        ],
        "Emerging and Developing Asia": [
            "Bangladesh", "Bhutan", "Brunei Darussalam", "Cambodia", "China, People's Republic of", "Fiji", "India",
            "Indonesia", "Kiribati", "Lao P.D.R.", "Malaysia", "Maldives", "Marshall Islands", "Micronesia, Fed. States of",
            "Mongolia", "Myanmar", "Nauru", "Nepal", "Palau", "Papua New Guinea", "Philippines", "Samoa",
            "Solomon Islands", "Sri Lanka", "Thailand", "Timor-Leste", "Tonga", "Tuvalu", "Vanuatu", "Vietnam"
        ],
        "Emerging and Developing Europe": [
            "Albania", "Belarus", "Bosnia and Herzegovina", "Bulgaria", "Hungary", "Kosovo", "Moldova", "Montenegro",
            "North Macedonia ", "Poland", "Romania", "Russian Federation", "Serbia", "Türkiye, Republic of", "Ukraine"
        ],
        "Emerging market and developing economies": [
            "Afghanistan", "Albania", "Algeria", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Azerbaijan",
            "Bahamas, The", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belize", "Benin", "Bhutan", "Bolivia",
            "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi",
            "Cabo Verde", "Cambodia", "Cameroon", "Central African Republic", "Chad", "Chile", "China, People's Republic of",
            "Colombia", "Comoros", "Congo, Dem. Rep. of the", "Congo, Republic of ", "Costa Rica", "Curacao",
            "Côte d'Ivoire", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
            "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Fiji", "Gabon", "Gambia, The", "Georgia", "Ghana",
            "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "India",
            "Indonesia", "Iran", "Iraq", "Jamaica", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait",
            "Kyrgyz Republic", "Lao P.D.R.", "Lebanon", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Malaysia",
            "Maldives", "Mali", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia, Fed. States of",
            "Moldova", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
            "Nicaragua", "Niger", "Nigeria", "North Macedonia ", "Oman", "Pakistan", "Palau", "Panama",
            "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Qatar", "Romania", "Russian Federation",
            "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "Saudi Arabia",
            "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Sint Maarten", "Solomon Islands", "Somalia",
            "South Africa", "South Sudan, Republic of", "Sri Lanka", "Sudan", "Suriname", "Syria", "São Tomé and Príncipe",
            "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
            "Turkmenistan", "Tuvalu", "Türkiye, Republic of", "Uganda", "Ukraine", "United Arab Emirates", "Uruguay",
            "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "West Bank and Gaza", "Yemen", "Zambia", "Zimbabwe"
        ],
        "Euro area": [
            "Austria", "Belgium", "Croatia", "Cyprus", "Estonia", "Finland", "France", "Germany", "Greece", "Ireland",
            "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Portugal", "Slovak Republic", "Slovenia",
            "Spain"
        ],
        "European Union": [
            "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland",
            "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta",
            "Netherlands", "Poland", "Portugal", "Romania", "Slovak Republic", "Slovenia", "Spain", "Sweden"
        ],
        "Latin America and the Caribbean": [
            "Antigua and Barbuda", "Argentina", "Bahamas, The", "Barbados", "Belize", "Bolivia", "Brazil", "Chile",
            "Colombia", "Costa Rica", "Curacao", "Dominica", "Dominican Republic", "Ecuador", "El Salvador", "Grenada",
            "Guatemala", "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru",
            "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Sint Maarten", "Suriname",
            "Trinidad and Tobago", "Uruguay", "Venezuela"
        ],
        "Major advanced economies (G7)": [
            "Canada", "France", "Germany", "Italy", "Japan", "United Kingdom", "United States"
        ],
        "Middle East and Central Asia": [
            "Afghanistan", "Algeria", "Armenia", "Azerbaijan", "Bahrain", "Djibouti", "Egypt", "Georgia", "Iran", "Iraq",
            "Jordan", "Kazakhstan", "Kuwait", "Kyrgyz Republic", "Lebanon", "Libya", "Mauritania", "Morocco", "Oman",
            "Pakistan", "Qatar", "Saudi Arabia", "Somalia", "Sudan", "Syria", "Tajikistan", "Tunisia", "Turkmenistan",
            "United Arab Emirates", "Uzbekistan", "West Bank and Gaza", "Yemen"
        ],
        "Other advanced economies": [
            "Andorra", "Australia", "Czech Republic", "Denmark", "Hong Kong SAR", "Iceland", "Israel",
            "Korea, Republic of", "Macao SAR", "New Zealand", "Norway", "Puerto Rico", "San Marino", "Singapore", "Sweden",
            "Switzerland", "Taiwan Province of China"
        ],
        "Sub-Saharan Africa": [
            "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", "Central African Republic",
            "Chad", "Comoros", "Congo, Dem. Rep. of the", "Congo, Republic of ", "Côte d'Ivoire", "Equatorial Guinea",
            "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia, The", "Ghana", "Guinea", "Guinea-Bissau", "Kenya",
            "Lesotho", "Liberia", "Madagascar", "Malawi", "Mali", "Mauritius", "Mozambique", "Namibia", "Niger",
            "Nigeria", "Rwanda", "Senegal", "Seychelles", "Sierra Leone", "South Africa", "South Sudan, Republic of",
            "São Tomé and Príncipe", "Tanzania", "Togo", "Uganda", "Zambia", "Zimbabwe"
        ],
            "World": [
            "Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla",
            "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan",
            "Bahamas, The", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda",
            "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "British Virgin Islands",
            "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon",
            "Canada", "Cayman Islands", "Central African Republic", "Chad", "Channel Islands", "Chile",
            "China, People's Republic of", "Colombia", "Comoros", "Congo, Dem. Rep. of the", "Congo, Republic of ",
            "Cook Islands", "Costa Rica", "Croatia", "Cuba", "Curacao", "Cyprus", "Czech Republic", "Côte d'Ivoire",
            "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
            "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Faeroe Islands",
            "Falkland Islands", "Fiji", "Finland", "France", "French Guiana", "French Polynesia", "Gabon",
            "Gambia, The", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada",
            "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Holy See",
            "Honduras", "Hong Kong SAR", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
            "Isle of Man", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
            "Korea, Dem. People's Rep. of", "Korea, Republic of", "Kosovo", "Kuwait", "Kyrgyz Republic",
            "Lao P.D.R.", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
            "Luxembourg", "Macao SAR", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
            "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico",
            "Micronesia, Fed. States of", "Moldova", "Monaco", "Mongolia", "Montenegro", "Montserrat",
            "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia",
            "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "North Macedonia ",
            "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
            "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar",
            "Reunion", "Romania", "Russian Federation", "Rwanda", "Saint Helena", "Saint Kitts and Nevis",
            "Saint Lucia", "Saint Martin", "Saint Vincent and the Grenadines", "Saint-Pierre and Miquelon",
            "Samoa", "San Marino", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
            "Singapore", "Sint Maarten", "Slovak Republic", "Slovenia", "Solomon Islands", "Somalia",
            "South Africa", "South Sudan, Republic of", "Spain", "Sri Lanka", "Sudan", "Suriname",
            "Svalbard and Jan Mayen Islands", "Sweden", "Switzerland", "Syria", "São Tomé and Príncipe",
            "Taiwan Province of China", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tokelau",
            "Tonga", "Trinidad and Tobago", "Tunisia", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu",
            "Türkiye, Republic of", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
            "United States", "United States Virgin Islands ", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela",
            "Vietnam", "Wallis and Futuna Islands", "West Bank and Gaza", "Western Sahara", "Yemen", "Zambia",
            "Zimbabwe"
        ]
    }

    country_regions_table = pd.DataFrame.from_dict(regions_mapping, orient='index').reset_index()
    country_regions_table = country_regions_table.melt(id_vars='index', var_name='id', value_name='country')
    country_regions_table.drop(columns=['id'], inplace=True)
    country_regions_table = (
        country_regions_table[~country_regions_table['country'].isnull()]
        .copy()
        .sort_values('index')
        .reset_index(drop=True)
    )
    country_regions_table.rename(columns={'index': 'Region', 'country': 'Country'}, inplace=True)

    country_analyticalgroups_table = pd.DataFrame.from_dict(analytical_group_mapping, orient='index').reset_index()
    country_analyticalgroups_table = country_analyticalgroups_table.melt(
        id_vars='index', var_name='id', value_name='country'
    )
    country_analyticalgroups_table.drop(columns=['id'], inplace=True)
    country_analyticalgroups_table = (
        country_analyticalgroups_table[~country_analyticalgroups_table['country'].isnull()]
        .copy()
        .sort_values('index')
        .reset_index(drop=True)
    )
    country_analyticalgroups_table.rename(columns={'index': 'Analytical Group', 'country': 'Country'}, inplace=True)

    return country_table, region_table, analytical_group_table, country_regions_table, country_analyticalgroups_table


def export_data(tables, file_names, script_dir):
    """Exports the tables to CSV files."""
    for i, table in enumerate(tables):
        file_name = file_names[i]
        path = os.path.join(script_dir, '../data/processed_norm/IMF Data normalized_' + file_name + '.csv')
        table.to_csv(path, index=False)


def main():
    """Main function to execute the pipeline."""
    script_dir = os.getcwd()
    main_file = os.path.join(script_dir, '../data/raw/IMF Data.xlsx')
    analytical_groups_file = os.path.join(script_dir, '../data/raw/IMF Data analytical-groups.xlsx')

    regions_df, countries_df, analytical_group_df = load_data(main_file, analytical_groups_file)

    if regions_df is None or countries_df is None or analytical_group_df is None:
        return  # Stop the process if there's an issue with loading the data.

    regions_df, countries_df, analytical_group_df = clean_data(regions_df, countries_df, analytical_group_df)
    regions_df, countries_df, analytical_group_df = reshape_data(regions_df, countries_df, analytical_group_df)

    country_table, region_table, analytical_group_table, country_regions_table, country_analyticalgroups_table = (
        create_normalized_tables(countries_df, regions_df, analytical_group_df)
    )

    tables = [
        country_table,
        region_table,
        country_regions_table,
        country_analyticalgroups_table,
        countries_df,
        regions_df,
        analytical_group_df,
    ]
    file_names = [
        'country_t',
        'region_t',
        'country_regions_t',
        'country_analyticalgroups_t',
        'countries_growth_t',
        'regions_growth_t',
        'analytical_groups_growth_t',
    ]

    export_data(tables, file_names, script_dir)

    print('Data preprocessing pipeline completed.')


if __name__ == '__main__':
    main()
