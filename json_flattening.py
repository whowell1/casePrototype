import json
import pandas as pd
from flatten_json import flatten

# Paths to the files
json_file_path = 'input.json'
csv_file_path = 'intermediate.csv'
flattened_csv_file_path = 'flattened_output.csv'

# Step 1: Read the JSON file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Step 2: Convert JSON to pandas DataFrame
df = pd.DataFrame(data)

# Step 3: Save initial DataFrame to CSV
df.to_csv(csv_file_path, index=False)

print(f"Initial CSV saved to {csv_file_path}")

# Display the columns to the user
print("Columns in the CSV file:")
print(df.columns)

# Step 4: Prompt the user to specify which column to flatten
column_to_flatten = input("Enter the column name to flatten: ")

# Step 5: Flatten the specified column
if column_to_flatten in df.columns:
    # Create a new DataFrame excluding the column to be flattened
    other_columns = df.drop(columns=[column_to_flatten])
    
    # Flatten the specified column and create a new DataFrame
    flattened_data = df[column_to_flatten].apply(lambda x: flatten(json.loads(x)) if isinstance(x, str) else flatten(x))
    flattened_df = pd.json_normalize(flattened_data)
    
    # Concatenate the original DataFrame with the flattened DataFrame
    final_df = pd.concat([other_columns, flattened_df], axis=1)
    
    # Step 6: Save the flattened DataFrame to a new CSV file
    final_df.to_csv(flattened_csv_file_path, index=False)
    
    print(f"Flattened CSV saved to {flattened_csv_file_path}")
else:
    print(f"Column '{column_to_flatten}' not found in the CSV file.")
