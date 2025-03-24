import csv
import json

def csv_to_json(csv_file_path):
    # Open the CSV file for reading
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        # Read the CSV file using DictReader to map columns to keys
        csv_reader = csv.DictReader(file)
        
        # Convert CSV rows into a list of dictionaries
        data = list(csv_reader)

    # Convert the list of dictionaries to a JSON object (string)
    json_data = json.dumps(data, indent=4)
    
    return json_data

def json_to_csv(csv_file_path, json_data):
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=json_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(json_data)

"""
def csv_to_json_file(csv_file_path, json_file_path):
    # Read the CSV file
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Convert to JSON and write to a file
        with open(json_file_path, 'w') as json_file:
            json.dump(list(csv_reader), json_file, indent=4)

"""

def json_to_csv_file(json_file_path, csv_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        
        # Write to CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data)

# Example usage
#json_to_csv('data.json', 'data.csv')
