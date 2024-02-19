import csv
import re
import os
import glob

def identify_columns(files, start_marker, end_marker):
    field_pattern = re.compile(r'(\w+)="[^"]*"')
    columns = set()
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            records = re.findall(re.escape(start_marker) + r'(.*?)' + re.escape(end_marker), content, re.DOTALL)
            for record in records:
                matches = field_pattern.findall(record)
                columns.update(matches)
    return list(columns)

start_marker = input("Please enter the initial string for a row entry: ")
ending_term = input("Please enter the ending term for each entry: ")

current_dir = os.getcwd()
input_dir = os.path.join(current_dir, 'input')
files = glob.glob(os.path.join(input_dir, '*'))
output_file_path = os.path.join(current_dir, 'output.csv')

column_names = identify_columns(files, start_marker, ending_term)

rows = []

for input_file_path in files:
    with open(input_file_path, 'r', encoding='utf-8') as txtfile:
        content = txtfile.read()
        records = re.findall(re.escape(start_marker) + r'(.*?)' + re.escape(ending_term), content, re.DOTALL)
        for record in records:
            current_record = {}
            for match in re.finditer(r'(\w+)="([^"]*)"', record):
                field_name, value = match.groups()
                current_record[field_name] = value
            rows.append(current_record)

# Write the data to a CSV file
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=column_names, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)
