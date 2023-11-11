import pandas as pd

# Load the data
file_path = './Datathon_Results_MOBILITY_2022_original_Students.xlsx'  # Replace with your actual file path
data = pd.read_excel(file_path)

# Define carbon-emitting transport modes
carbon_transport_modes = [
    'Combustion vehicle (non-plug-in hybrid, electric or plug-in hybrid with non-renewable source charging)',
    'Combustion or electric motorcycle with non-renewable source charging'
]

# Classify transport modes into non-carbon and carbon-emitting
data['Carbon_Emitting_Transport_Used'] = data[
    ['Indicate the modes of transport you use to go to the UPC. (only mark the stages that last more than 5 minutes, up to a maximum of 3 stages) [Stage 1]',
     'Indicate the modes of transport you use to go to the UPC. (only mark the stages that last more than 5 minutes, up to a maximum of 3 stages) [Stage 2]',
     'Indicate the modes of transport you use to go to the UPC. (only mark the stages that last more than 5 minutes, up to a maximum of 3 stages) [Stage 3]']
].apply(lambda x: any(mode in carbon_transport_modes for mode in x), axis=1)

# Filter out the data for carbon-emitting transport users
carbon_emitters = data[data['Carbon_Emitting_Transport_Used']]

# Modify the postal codes to have a 0 as the last digit
carbon_emitters['Postal_Code_Modified'] = carbon_emitters['Please indicate the postal code from where you usually start your trip to the university:'] \
                                            .apply(lambda x: str(int(x)).zfill(5)[:-1] + '0' if pd.notnull(x) else x)

# Group by faculty and count the occurrences of each modified postal code
postal_codes_counts_by_faculty = carbon_emitters.groupby(['Select the center where you study:', 'Postal_Code_Modified']).size().reset_index(name='Count')

# Pivot the table to have faculties as rows and postal codes as columns filled with counts
pivot_postal_codes_by_faculty = postal_codes_counts_by_faculty.pivot(index='Select the center where you study:', columns='Postal_Code_Modified', values='Count').fillna(0)

# Sort the postal codes by count and take the top 10 for each faculty
top_10_postal_codes_by_faculty = pivot_postal_codes_by_faculty.apply(lambda x: x.sort_values(ascending=False).head(10).index, axis=1)

# Convert the series to a DataFrame
top_10_postal_codes_df = top_10_postal_codes_by_faculty.apply(pd.Series).reset_index()
top_10_postal_codes_df.columns = ['Faculty', '1st Postal Code', '2nd Postal Code', '3rd Postal Code', '4th Postal Code', '5th Postal Code', '6th Postal Code', '7th Postal Code', '8th Postal Code', '9th Postal Code', '10th Postal Code']

# Save the DataFrame to a CSV file
csv_file_path_top_10_modified = './top_10_modified_postal_codes_by_faculty.csv'
top_10_postal_codes_df.to_csv(csv_file_path_top_10_modified, index=False)
