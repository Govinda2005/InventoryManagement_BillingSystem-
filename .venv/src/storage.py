# src/storage.py
import csv
import os
from tempfile import NamedTemporaryFile

def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(path, fieldnames, rows):
    # safe write
    tmp = NamedTemporaryFile('w', delete=False, newline='', encoding='utf-8')
    try:
        writer = csv.DictWriter(tmp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    finally:
        tmp.close()
        os.replace(tmp.name, path)
