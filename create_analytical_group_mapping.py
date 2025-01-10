if __name__ == "__main__":

    import pandas as pd

    # Dictionary mapping different analytical groups to lists of their member countries
    # Each key is a group name (e.g. "ASEAN-5", "Euro area") and value is a list of countries
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

    # Convert the nested dictionary structure into a pandas DataFrame
    # orient='index' makes dictionary keys become DataFrame index
    analytical_group_mapping_df = pd.DataFrame.from_dict(analytical_group_mapping, orient='index').reset_index()

    # Reshape DataFrame from wide to long format
    # Each country gets its own row, with the group name in 'index' column
    analytical_group_mapping_df = analytical_group_mapping_df.melt(id_vars='index', var_name='id', value_name='country')

    # Remove the unnecessary 'id' column that was created during melting
    analytical_group_mapping_df.drop(columns=['id'], inplace=True)

    # Clean up the DataFrame:
    # 1. Remove rows with null country values
    # 2. Sort by group name ('index' column)
    # 3. Reset the index to get clean row numbers
    analytical_group_mapping_df = analytical_group_mapping_df[~analytical_group_mapping_df['country'].isnull()].copy().sort_values('index').reset_index(drop=True)

    # Save the final DataFrame to a CSV file in the data/processed directory
    analytical_group_mapping_df.to_csv('data/processed/analytical_group_mapping.csv', index=False)