import csv
import os

# read csv file logic
def read_csv(filename):
    """Read data from a CSV file and return a list of dictionaries."""
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


# write to a csv file logic
def write_csv(filename, fieldnames, data):
    """Write a list of dictionaries to a CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# appending to csv file logic
def append_csv(filename, fieldnames, row):
    """Append a single dictionary row to an existing CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
