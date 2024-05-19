import sqlite3
import csv

# Define the path to the SRUM database
srum_db_path = r"C:\Windows\System32\sru\SRUM.db"

# Define the output CSV file path
output_csv_path = r"C:\path\to\SRUM.csv"

# Connect to the SQLite database
conn = sqlite3.connect(srum_db_path)
cursor = conn.cursor()

# Retrieve the list of tables in the SRUM database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Open the CSV file for writing
with open(output_csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    for table in tables:
        table_name = table[0]
        
        # Write the table name as a header
        writer.writerow([f"Table: {table_name}"])
        
        # Get the column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        writer.writerow(column_names)
        
        # Get the table data
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        for row in rows:
            writer.writerow(row)
        
        # Write an empty line to separate tables in the CSV
        writer.writerow([])

# Close the database connection
conn.close()

print(f"Export completed. The data has been saved to {output_csv_path}")
