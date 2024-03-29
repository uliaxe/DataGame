import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # Read CSV file
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
    
    # Write JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
csv_file_path = 'vgsales.csv'
json_file_path = 'vgsales.json'
csv_to_json(csv_file_path, json_file_path)
